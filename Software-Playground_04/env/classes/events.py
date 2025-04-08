class StopEvent:
    def __init__(self) -> None:
        self._is_set: bool = False

    def set(self)    -> None: self._is_set = True
    def reset(self)  -> None: self._is_set = False
    def is_set(self) -> bool: return self._is_set
