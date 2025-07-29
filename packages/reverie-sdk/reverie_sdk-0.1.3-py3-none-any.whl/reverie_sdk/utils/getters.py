import typing


def dict_alt_getter(d: typing.Dict, keys: typing.List):
    for key in keys:
        if key in d:
            return d[key]

    return None


def chain_getter(d: typing.Union[typing.Dict, typing.List], keys: typing.List):
    success = True
    for key in keys:
        try:
            d = d[key]
        except Exception:
            success = False
            break

    return d if success else None
