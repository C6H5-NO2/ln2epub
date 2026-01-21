class __AttrSetter:
    def __init__(self, obj):
        self.__obj = obj

    def __setattr__(self, name, value):
        object.__setattr__(self.__obj, name, value)


def _attr_setter[T](_self: T, /) -> T:
    return __AttrSetter(_self)
