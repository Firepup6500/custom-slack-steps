def toBool(thing: any) -> bool:
    if type(thing) == str:
        return thing.lower() in ["yes", "true", "on", "one", "1", "y", "t"]
    return bool(thing)
