from collections.abc import Callable, Iterable, Iterator, MutableMapping
from typing import Any, cast


class CRUDLWrapper[KT: Any, VT: Any]:
    def __init__(self, mapping: MutableMapping[KT, VT]) -> None:
        self.mapping = mapping

    def create(self, key: KT, value: VT) -> VT:
        if key in self.mapping:
            raise KeyError

        self.mapping[key] = value
        return value

    def read(self, key: KT) -> VT:
        return self.mapping[key]

    def update(self, key: KT, value: VT) -> VT:
        if key not in self.mapping:
            raise KeyError

        self.mapping[key] = value
        return value

    def delete(self, key: KT) -> VT:
        default = object()
        value = self.mapping.pop(key, default)
        if value == default:
            raise KeyError

        return cast("VT", value)

    def list(self) -> Iterable[tuple[KT, VT]]:
        return self.mapping.items()


class CRUDLDict[KT: Any, VT: Any](MutableMapping[KT, VT]):
    def __init__(
        self,
        *,
        create_func: Callable[[KT | None, Any], VT | None],
        read_func: Callable[[KT], VT],
        update_func: Callable[[KT, Any], VT | None],
        delete_func: Callable[[KT], VT | None],
        list_func: Callable[[], Iterable[tuple[KT, VT | None]]],
    ) -> None:
        self.__create_func = create_func
        self.__read_func = read_func
        self.__update_func = update_func
        self.__delete_func = delete_func
        self.__list_func = list_func

    def __delitem__(self, key: KT) -> None:
        self.__delete_func(key)

    def __getitem__(self, key: KT) -> VT:
        return self.__read_func(key)

    def __setitem__(self, key: KT | None, value: VT) -> None:
        if key is None or key not in self:
            self.__create_func(key, value)
        else:
            self.__update_func(key, value)

    def __iter__(self) -> Iterator[KT]:
        for key, _ in self.__list_func():
            yield key

    def __len__(self) -> int:
        # Cannot use `count` in `toolz` as itself depends on this function
        count = 0
        for _ in self:
            count += 1
        return count
