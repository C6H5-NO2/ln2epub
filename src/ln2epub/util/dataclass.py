def _attr_setter[T](_self: T, /) -> T:
    class AttrSetter:
        def __setattr__(self, name, value):
            object.__setattr__(_self, name, value)

    return AttrSetter()
