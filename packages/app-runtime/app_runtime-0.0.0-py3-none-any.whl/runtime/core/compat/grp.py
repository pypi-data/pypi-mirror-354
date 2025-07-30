# compatability classes, variables and functions for the grp module on linux

class Group: # pragma: no cover

    @property
    def gr_gid(self) -> int:
        ...

    @property
    def gr_name(self) -> str:
        ...

    @property
    def gr_mem(self) -> list[str]:
        ...

def getgrall() -> list[Group]: # pragma: no cover
    raise NotImplementedError