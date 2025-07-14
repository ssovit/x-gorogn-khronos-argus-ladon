import sys
import os


class Colors:
    red = (245, 90, 66)
    orange = (245, 170, 66)
    yellow = (245, 252, 71)
    green = (92, 252, 71)
    blue = (71, 177, 252)
    purple = (189, 71, 252)
    white = (255, 255, 255)


class ColorsFG:
    Black = "\033[30m"
    Red = "\033[31m"
    Green = "\033[32m"
    Yellow = "\033[33m"
    Blue = "\033[34m"
    Magenta = "\033[35m"
    Cyan = "\033[36m"
    White = "\033[37m"
    BrighBlack = "\033[90m"
    BrightRed = "\033[91m"
    BrightGreen = "\033[92m"
    BrightYellow = "\033[93m"
    BrightBlue = "\033[94m"
    BrightMagenta = "\033[95m"
    BrightCyan = "\033[96m"
    BrightWhite = "\033[97m"


class ColorsBG:
    Black = "\033[40m"
    Red = "\033[41m"
    Green = "\033[42m"
    Yellow = "\033[43m"
    Blue = "\033[44m"
    Magenta = "\033[45m"
    Cyan = "\033[46m"
    White = "\033[47m"
    BrighBlack = "\033[100m"
    BrightRed = "\033[101m"
    BrightGreen = "\033[102m"
    BrightYellow = "\033[103m"
    BrightBlue = "\033[104m"
    BrightMagenta = "\033[105m"
    BrightCyan = "\033[106m"
    BrightWhite = "\033[107m"


def init_colorit():
    if sys.platform.startswith("win32"):
        os.system("cls")
    elif sys.platform.startswith("darwin") or sys.platform.startswith("linux"):
        os.system("clear")


def color(text, rgb):
    return "\033[38;2;{};{};{}m{}\033[0m".format(
        str(rgb[0]), str(rgb[1]), str(rgb[2]), text
    )


def color_ansi(text, color):
    return "{}{}\033[0m".format(color, text)


def background(text, rgb):
    return "\033[48;2;{};{};{}m{}\033[0m".format(
        str(rgb[0]), str(rgb[1]), str(rgb[2]), text
    )
