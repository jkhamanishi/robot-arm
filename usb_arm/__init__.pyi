from usb_signals import BitPattern
from usb.core import Device
from typing import Callable

class _Move:
    def __init__(self, move_function: Callable[[BitPattern, float], None], message: BitPattern) -> None: ...
    def __call__(self, time: float = ...) -> None: ...
    def __or__(self, other) -> None: ...

class _Actuator: ...

class _EndEffector(_Actuator):
    open: _Move
    close: _Move

class _Joint(_Actuator):
    up: _Move
    down: _Move

class _Base(_Actuator):
    cw: _Move
    ccw: _Move

class _LED(_Actuator):
    on: _Move
    off: _Move

class Arm(object):
    dev: Device
    grippers: _EndEffector
    wrist: _Joint
    elbow: _Joint
    shoulder: _Joint
    base: _Base
    led: _LED
    def __init__(self) -> None: ...
    def _tell(self, message: BitPattern) -> None: ...
    def stop(self) -> None: ...
    def move(self, pattern: BitPattern, time: float = ...) -> None: ...
    def blink(self, count: int = 5) -> None: ...
    def block_left(self) -> None: ...
    def block_right(self) -> None: ...
