class frozendict(dict) :

    """
    Quick and easy implementation of an immutable and hashable dictionnary.
    I mostly need it to be hashable in order to memoize using 'functools.lru_cache'.
    The name 'frozendict' come from PEP 416.
    """

    def __repr__(self) -> str:
        return f"frozendict({super().__repr__()})"

    def __setitem__(self, key, value) :
        raise TypeError("Frozendict are immutable")
    
    def __delitem__(self, key) :
        raise TypeError("Frozendict are immutable")

    def __hash__(self) -> int:
        return hash(tuple(self.items()))

    def unfreeze(self) -> dict:
        return dict(self.items())
