from typing import Optional


def all_optional(cls):
    for name, field in cls.__annotations__.items():
        if name.startswith("__"):
            continue
        cls.__annotations__[name] = Optional[field]
    return cls
