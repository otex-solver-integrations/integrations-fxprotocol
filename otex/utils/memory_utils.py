from typing import Any

class StatesBuffer:

    def __init__(self) -> None:
        pass

    def to_dict(
        self
    ):
        return self.__dict__

    def add_state(
        self,
        name: str,
        value: Any
    ):
        setattr(self, name, value)
    