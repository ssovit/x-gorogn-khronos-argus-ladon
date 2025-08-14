from base64 import b64encode
from hashlib import md5
import hashlib
from random import randint, random
from struct import unpack
from time import time
from urllib.parse import parse_qs

from Crypto.Cipher.AES import MODE_CBC, block_size, new
from Crypto.Util.Padding import pad

from .protobuf import ProtoBuf
from .Simon import simon_enc
from .Sm3 import SM3


class Argus:
    def encrypt_enc_pb(data, l):
        data = list(data)
        xor_array = data[:8]

        for i in range(8, l):
            data[i] ^= xor_array[i % 8]

        return bytes(data[::-1])

    @staticmethod
    def calculate_constant(code):
        parts = [int(digit) for digit in code.replace(".", "").zfill(6)]
        return sum(
            part * weight
            for part, weight in zip(
                parts, [20480, 2048, 20971520, 2097152, 1342177280, 134217728]
            )
        )

    @staticmethod
    def get_bodyhash(stub: str | None = None) -> bytes:
        return (
            SM3().sm3_hash(bytes(16))[0:6]
            if stub == None or len(stub) == 0
            else SM3().sm3_hash(bytes.fromhex(stub))[0:6]
        )

    @staticmethod
    def get_queryhash(query: str) -> bytes:
        if not isinstance(query, str):
            raise ValueError("query must be a string")
        return (
            SM3().sm3_hash(bytes(16))[0:6]
            if query == None or len(query) == 0
            else SM3().sm3_hash(query.encode())[0:6]
        )

    @staticmethod
    def encrypt(xargus_bean: dict):
        protobuf = pad(bytes.fromhex(ProtoBuf(xargus_bean).toBuf().hex()), block_size)
        new_len = len(protobuf)
        sign_key = b"\xac\x1a\xda\xae\x95\xa7\xaf\x94\xa5\x11J\xb3\xb3\xa9}\xd8\x00P\xaa\n91L@R\x8c\xae\xc9RV\xc2\x8c"
        sm3_output = b"\xfcx\xe0\xa9ez\x0ct\x8c\xe5\x15Y\x90<\xcf\x03Q\x0eQ\xd3\xcf\xf22\xd7\x13C\xe8\x8a2\x1cS\x04"  # sm3_hash(sign_key + b'\xf2\x81ao' + sign_key)

        key = sm3_output[:32]
        key_list = []
        enc_pb = bytearray(new_len)

        for _ in range(2):
            key_list = key_list + list(unpack("<QQ", key[_ * 16 : _ * 16 + 16]))

        for _ in range(int(new_len / 16)):
            pt = list(unpack("<QQ", protobuf[_ * 16 : _ * 16 + 16]))
            ct = simon_enc(pt, key_list)
            enc_pb[_ * 16 : _ * 16 + 8] = ct[0].to_bytes(8, byteorder="little")
            enc_pb[_ * 16 + 8 : _ * 16 + 16] = ct[1].to_bytes(8, byteorder="little")

        b_buffer = Argus.encrypt_enc_pb(
            (b"\xf2\xf7\xfc\xff\xf2\xf7\xfc\xff" + enc_pb), new_len + 8
        )
        b_buffer = b"\xa6n\xad\x9fw\x01\xd0\x0c\x18" + b_buffer + b"ao"

        cipher = new(md5(sign_key[:16]).digest(), MODE_CBC, md5(sign_key[16:]).digest())

        return b64encode(
            b"\xf2\x81" + cipher.encrypt(pad(b_buffer, block_size))
        ).decode("utf-8")

    @staticmethod
    def get_sign(
        params: None | str = None,
        stub: None | str = None,
        timestamp: int = int(time()),
        aid: int = 1233,
        license_id: int = 1611921764,
        platform: int = 0,
        channel="googleplay",
        sec_device_id: str = None,
        sdk_version: str = "v04.04.05-ov-android",
        sdk_version_int: int = 134744640,
        lanusk=None,
        lanusk_version=None,
        seed_token=None,
        seed_version=None,
    ):
        params_dict = parse_qs(params)
        argus_bean = {
            1: 0x20200929 << 1,  # magic
            2: 2,  # version
            3: randint(0, 0x7FFFFFFF),  # rand
            4: str(aid),  # msAppID
            5: params_dict.get("device_id",[None])[0],  # deviceID
            6: str(license_id),  # licenseID
            7: params_dict.get("version_name",[None])[0],  # appVersion
            8: sdk_version,  # sdkVersionStr
            9: sdk_version_int,  # sdkVersion
            10: bytes(8),  # envcode -> jailbreak Detection
            11: platform,  # platform (ios = 1)
            12: timestamp << 1,  # createTime
            13: Argus.get_bodyhash(stub),  # bodyHash
            14: Argus.get_queryhash(params),  # queryHash
            # 15: {
            #     1: random.randint(10, 100),
            #     2: random.randint(10, 100),
            #     3: random.randint(10, 100),
            #     5: random.randint(10, 100),
            #     6: random.randint(10, 100) * 2,
            #     7: (timestamp - 240) << 1,
            # },
        }
        if sec_device_id:
            argus_bean[16] = sec_device_id
        # argus_bean[17] = timestamp << 1
        if lanusk and lanusk_version:
            argus_bean[18] = bytes.fromhex(
                hashlib.md5(lanusk.encode("utf-8")).hexdigest()
            )
            argus_bean[19] = SM3().sm3_hash(
                bytes.fromhex(
                    params.encode("utf-8").hex()
                    + stub
                    + lanusk_version.encode("utf-8").hex()
                )
            )
            argus_bean[20] = lanusk_version
        else:
            argus_bean[20] = "none"
        argus_bean[20] = 738
        argus_bean[23] = {
            1: str(params_dict.get("device_type", [""])[0]),
            2: params_dict.get("os_version", [""])[0],
            3: channel,
            4: Argus.calculate_constant(params_dict.get("os_version", [""])[0]),
        }
        if seed_token and seed_version:
            argus_bean[24] = str(seed_token)
            argus_bean[25] = random.choice([2, 6, 8, 10])
            argus_bean[26] = {1: int(seed_version) << 1, 2: seed_version}
        return Argus.encrypt(argus_bean)


if __name__ == "__main__":

    print(
        Argus.get_sign(
            params="user_id=6928026132446266374&sec_user_id=MS4wLjABAAAAR9MfYTvIWfBW_EvwHGL7lkY_ff8BsPIujg3UPwPGacX5Q2UMVPiNGjYpDv1ux68Z&manifest_version_code=2023009040&app_language=en&app_type=normal&iid=7410429761295550214&channel=googleplay&device_type=SM-A127F&language=en&cpu_support64=true&host_abi=armeabi-v7a&locale=en&resolution=1467x720&openudid=94f7525e8469e214&update_version_code=2023009040&ac2=wifi&cdid=b1814d42-f71b-4ee3-8019-1b5c0099c912&sys_region=US&os_api=29&uoo=0&timezone_name=America%2FLos_Angeles&dpi=300&ac=wifi&device_id=7410428789866563078&os_version=10&timezone_offset=-25200&version_code=300904&app_name=musical_ly&ab_version=30.9.4&version_name=30.9.4&device_brand=samsung&op_region=US&ssmix=a&device_platform=android&build_number=30.9.4&region=US&aid=1233&ts=1726722185&_rticket=1726722185321",
            stub=None,
            timestamp=1726722185,
            platform=0,
            aid=1233,
            license_id=1611921764,
            sec_device_id="",
            sdk_version="v04.04.05-ov-android",
            sdk_version_int=134744640,
        )
    )
