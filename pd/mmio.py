from typing import Tuple, List, Dict  # noqa


def _verify_args(types, args):
    if len(args) != len(types):
        return False
    if not all([isinstance(args[i], types[i]) for i in range(len(types))]):
        return False
    return True


class MemoryTree():
    def __init__(self):
        self._size: int = 0  # 0:auto
        self._addr: int = 0  # 0:auto
        self.children: List[MemoryTree] = list()

    @property
    def size(self):
        if self._size > 0:
            return self._size
        if len(self.children) == 0:
            return self._size
        start = self.children[0].addr
        end = self.children[-1].addr + self.children[-1].size
        size = end - start
        return size

    @property
    def absaddr(self):
        return self._addr

    def insert(self, idx: int, obj: object) -> None:
        # check if obj can be inserted
        pass
        # insert
        self.children.insert(idx, obj)
        # calc addr if obj.addr is 'auto'
        if obj.addr == 0:
            prev = self.children[idx - 1]
            obj.addr = prev.addr + prev.size


class RegisterMap():
    def __init__(self, *args):
        addr, name = int(), str()
        if _verify_args([int, str], args):
            addr, name = args
        self.addr: int = addr
        self.size: int = 0
        self.name: str = name or str()
        self.description: str = str()
        self.access: str = str()
        self._section: List[RegisterSection] = list()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._section[key]
        elif isinstance(key, str):
            for s in self._section:
                if key in s.name:
                    return s
            else:
                raise KeyError()
        raise KeyError()

    def __setitem__(self, key, value):
        self._section[key] = value

    def __iadd__(self, other):
        if isinstance(other, RegisterSection):
            self._section.append(other)
            pass
        else:
            raise Exception()
        return self


class RegisterSection():
    def __init__(self, *args):
        addr, size, name = -1, -1, str()
        if _verify_args([int, str], args):
            addr, name = args
        elif _verify_args([int, int, str], args):
            addr, size, name = args
        elif _verify_args([list, str], args) and _verify_args([int, int], args[0]):
            a0, name = args
            addr = a0[0]
            size = a0[1] - a0[0] + 1
        self.baseaddr: int = addr
        self.size: int = size
        self.name: str = name or str()
        self.description: str = str()
        self.access: str = str()
        self._register: List[Register] = list()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._register[key]
        elif isinstance(key, str):
            for reg in self._register:
                if key in reg.name:
                    return reg
            else:
                raise KeyError()
        raise KeyError()

    def __setitem__(self, key, value):
        self._register[key] = value

    def __iadd__(self, other):
        if isinstance(other, Register):
            self._register.append(other)
            pass
        else:
            raise Exception()
        return self


class Register():
    def __init__(self, *args, **kwargs):
        addr, size, name = -1, -1, str()
        if _verify_args([int, str], args):
            addr, name = args
        elif _verify_args([int, int, str], args):
            addr, size, name = args
        elif _verify_args([list, str], args) and _verify_args([int, int], args[0]):
            a0, name = args
            addr = a0[0]
            size = a0[1] - a0[0] + 1
        self.offset: int = addr
        self.size: int = size
        self.name: str = name or str()
        self.description: str = str()
        self.width: int = 32
        self.access: str = str()
        self._field: List[Field] = list()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._field[key]
        elif isinstance(key, str):
            for field in self._field:
                if key in field.name:
                    return field
            else:
                raise KeyError()
        raise KeyError()

    def __setitem__(self, key, value):
        if value in self._field:
            return

    def __iadd__(self, other):
        if isinstance(other, Field):
            self._field.append(other)
            pass
        else:
            raise Exception()
        return self


class Field():
    def __init__(self, *args, **kwargs):
        bits, name = bit_[:], str()
        if _verify_args([Bit.Slice, str], args):
            bits, name = args
        self.name: str = name
        self.description: str = str()
        self.bits: Tuple[int] = tuple()
        self.access: str = str()
        self.resetvalue: Tuple[int] = tuple()
        self._children: List[Field] = list()

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._field[key]
        elif isinstance(key, str):
            for field in self._children:
                if key in field.name:
                    return field
            else:
                raise KeyError()
        raise KeyError()

    def __setitem__(self, key, value):
        if value in self._children:
            return

    def __iadd__(self, other):
        if isinstance(other, Field):
            self._children.append(other)
            pass
        else:
            raise Exception()
        return self


class Const():
    def __init__(self, name, value):
        self.name: str = name
        self.value: int = value


class Enum():
    def __init__(self, name):
        self.name: str = name
        self.values: Dict[str, int] = dict()


class Bit():
    class Slice():
        def __init__(self, key):
            self.key = key

    def __getitem__(self, key):
        return Bit.Slice(key)


bit_ = Bit()
