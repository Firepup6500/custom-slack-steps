from typing import Any


def toBool(thing: Any) -> bool:
    if type(thing) == str:
        return thing.lower() in ["yes", "true", "on", "one", "1", "y", "t"]
    return bool(thing)
