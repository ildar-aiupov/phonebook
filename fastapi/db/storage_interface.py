from abc import ABC, abstractmethod

from typing import Any


class StorageInterface(ABC):
    @abstractmethod
    async def get_entry(self, key: Any) -> Any | None:
        ...

    @abstractmethod
    async def set_entry(self, key: Any, value: Any) -> None:
        ...
