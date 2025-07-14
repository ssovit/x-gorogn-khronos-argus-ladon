import time

from .XArgus import Argus
from .XLadon import Ladon

from .XGorgon import XGorgon



def Sign(
    params: str,
    headers: dict = {},
    sec_device_id: str = "",
    aid: int = 1233,
    license_id: int = 1611921764,
    sdk_version_str: str = "v04.04.05-ov-android",
    sdk_version: int = 134744640,
    platform: int = 0,
    unix: int = None,
):
    x_ss_stub = None
    if "x-ss-stub" in headers:
        x_ss_stub = headers["x-ss-stub"]
    if not unix:
        unix = int(time.time())
    return {**headers,
            **XGorgon().calculate(params=params, headers=headers),
            **{
                "x-ladon": Ladon.encrypt(unix, license_id, aid),
                "x-argus": Argus.get_sign(
                    params,
                    x_ss_stub,
                    unix,
                    platform=platform,
                    aid=aid,
                    license_id=license_id,
                    sec_device_id=sec_device_id,
                    sdk_version=sdk_version_str,
                    sdk_version_int=sdk_version,
                ),
            }}
