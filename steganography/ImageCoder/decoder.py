from pathlib import Path
from sys import exit
from PIL import Image
from ImageCoder import TERMINATION

t = "".join([format(ord(char), '08b') for char in TERMINATION])


def decode(image: Image) -> dict:
    return {"message": _decode_message(image)}


def _decode_message(image: Image) -> str:
    width, height = image.size
    msg = ""

    for x in range(width):
        if _check_termination(msg): break
        for y in range(height):
            if _check_termination(msg): break
            pixel = list(image.getpixel((x, y)))
            for i in range(3):
                if _check_termination(msg): break
                msg += _get_bit(pixel[i])
    return _bin_to_msg(msg[:-len(t)])


def _check_termination(msg: str) -> bool:
    return msg[-len(t):] == t and len(msg) % 8 == 0


def _get_bit(number: int) -> str:
    return str(number & 1)


def _bin_to_msg(binary_str: str) -> str:
    if len(binary_str) % 8 != 0:
        raise ValueError("Invalid binary string length. It should be a multiple of 8.")

    binary_segments = [binary_str[i:i + 8] for i in range(0, len(binary_str), 8)]

    ascii_str = "".join(chr(int(segment, 2)) for segment in binary_segments)

    return ascii_str
