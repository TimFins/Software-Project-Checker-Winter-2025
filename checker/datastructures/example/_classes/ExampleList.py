from __future__ import annotations

class ExampleList:
    """Class representing an example list."""

    def __init__(self, data: list|None=None):
        if not isinstance(data, list) and data is not None:
             raise ValueError(
                "Invalid data format: the data is not list and not None.")
        
        if not data:
            self._data = []
        else:
            self._data = data

    def __repr__(self) -> str:
        return f"ExampleList={str(self._data)}"
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExampleList):
            return NotImplemented
        return self._data == other._data

    def get_data(self) -> list:
        return self._data

    def sorted(self, sort_ascending: bool = True) -> ExampleList:
        return ExampleList(sorted(self._data, reverse=not sort_ascending))
