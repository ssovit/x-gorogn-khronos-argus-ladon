import binascii
import hashlib
import json
import random
import time
from typing import Union  # Make sure to import Union for the type hint

def trace_id(device_id: Union[str, int] = "") -> str:
    """
    Generates a unique trace ID similar to a UUID format, possibly used for request tracking.

    Parameters:
    - device_id (str or int): Optional device identifier. If empty, a timestamp-based ID is generated.

    Returns:
    - str: A formatted trace ID like "00-<main_id>-<short_id>-01"
    """
    if device_id == "":
        # Use current time in milliseconds if no device_id is provided
        device_id = str(round(time.time()*1000)).zfill(9)

    # Get current time in milliseconds modulo 2^32, convert to hex and pad to 8 characters
    e = toHexStr(round(time.time()*1000) % 4294967295).zfill(8)

    # Determine if device_id is numeric or a string
    if type(device_id) == int:
        r = "01"
    else:
        device_id = device_id.replace("-", "")
        r = int(device_id)

    # Convert device ID to hex
    e2 = toHexStr(r)

    # Calculate how many more characters are needed for the ID seed
    r = 22 - len(e2) - 4

    # Encode the length of e2 as a 2-digit string
    c = str(len(e2)).zfill(2)

    # Create a random seed (hex), truncated to required length
    seed = toHexStr(round(random.random() * pow(10, 12)))[0:r]

    # Construct full ID body
    c = c + e2 + seed
    e3 = e + c
    e3_1 = e3[0:16]

    # Return final trace ID
    res = f"00-{e3}-{e3_1}-01"
    return res


def json_encode(data: dict) -> str:
    """
    Encodes a Python dictionary to a compact JSON string.

    Parameters:
    - data (dict): The dictionary to encode.

    Returns:
    - str: Minified JSON string.
    """
    return json.dumps(data, separators=(",", ":"), indent=None)


def md5stub(body) -> str:
    """
    Computes the uppercase MD5 hash of a string or bytes.

    Parameters:
    - body (str or bytes): The content to hash.

    Returns:
    - str: The MD5 hash in uppercase.
    """
    try:
        return (hashlib.md5(body).hexdigest()).upper()
    except:
        return (hashlib.md5(body.encode()).hexdigest()).upper()


def xor(data, key=5):
    """
    Performs XOR obfuscation on a string with a static key and returns it as a hex string.

    Parameters:
    - data (str): The string to obfuscate.
    - key (int): The XOR key (default is 5).

    Returns:
    - str: Hex-encoded XORed string.
    """
    i = 0
    datas = ""
    while i < len(data):
        # XOR each character with key and convert to hex
        datas = datas + binascii.hexlify(bytes(chr(ord(data[i]) ^ key), "UTF-8")).decode()
        i = i + 1
    return datas

def getUNIX(add: bool = False, addRandom: int = 0) -> int:
    if add:
        return int(round((time.time() * 1000)) + addRandom)
    else:
        return int(round(time.time()))