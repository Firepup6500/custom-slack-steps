#!/usr/bin/python3
from typing import Any


def toBool(thing: Any) -> bool:
    if type(thing) == str:
        return thing.lower() in ["yes", "true", "on", "one", "1", "y", "t"]
    return bool(thing)


def blacklist(userid: str):
    return userid not in [
        "U08BFAYDQ49",
        "U0782516RDE",
        "U07B4QD9F61",
        "U061GB9JUP7",
        "U06LWT5MHGQ",
        "U07373D8R7X",
        "U0890970LUT",
        "U07LEF1PBTM",
        "U080S1GNHNK",
        "U036UQD2893",
        "U07NJEABDGV",
        "U012K5ASJ90",
        "U0851ALFKTR",
        "U08DX7KD5K3",
        "UM1L1C38X",
        "U06MENEABV4",
        "U019S6AH18F",
        "U06MJDZHTK7",
        "U08B8USKT29",
        "U07ATH6TW95",
        "U078FB76K5F",
        "U07NGBJUDRD",
        "U07NVCHT6TZ",
        "U071THMU8HH",
    ]
