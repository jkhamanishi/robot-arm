"""
Maplin/OWI USB Robot arm control.

Code derrived from python_usb_robot_arm by orionrobots

Usage:

>>> import usb_arm
>>> arm = usb_arm.Arm()
>>> arm.grippers.open()
>>> arm.block_left()  # WARNING - ARM SHOULD BE ALL THE WAY RIGHT BEFORE TRYING THIS

"""

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
    """Arm interface"""
    dev: Device
    grippers: _EndEffector
    wrist: _Joint
    elbow: _Joint
    shoulder: _Joint
    base: _Base
    led: _LED
    def __init__(self) -> None: ...
    def tell(self, message: BitPattern) -> None:
        """Send a USB message to the arm"""
    def stop(self) -> None: ...
    def move(self, pattern: BitPattern, time: float = ...) -> None:
        """Perform a pattern move with timing and stop"""
    def blink(self, count: int = 5) -> None:
        """Blink the LED on the arm. By default, five times."""
    def block_left(self) -> None: ...
    def block_right(self) -> None: ...
