"""
Maplin/OWI USB Robot arm control.

Code derrived from python_usb_robot_arm by orionrobots

Usage:

>>> import usb_arm
>>> arm = usb_arm.Arm()
>>> arm.grippers.open()
>>> arm.block_left()  # WARNING - ARM SHOULD BE ALL THE WAY RIGHT BEFORE TRYING THIS

"""

import usb_arm.usb_signals as msg
import usb.core
from time import sleep
from typing import Callable

DEFAULT_DURATION = 1  # seconds


class _Move:
    def __init__(self, move_function: Callable[[msg.BitPattern, float], None], message: msg.BitPattern):
        self.move = move_function
        self.message = message

    def __call__(self, time: float = DEFAULT_DURATION):
        self.move(self.message, time)

    def __or__(self, other):
        return _Move(self.move, self.message | other.message)

    def __repr__(self):
        return "<_Move message:%s>" % self.message

    def __str__(self):
        return self.__repr__()


class _Actuator:
    pass


class _EndEffector(_Actuator):
    def __init__(self, move_function: Callable, open_msg: msg.BitPattern, close_msg: msg.BitPattern):
        self.open = _Move(move_function, open_msg)
        self.close = _Move(move_function, close_msg)


class _Joint(_Actuator):
    def __init__(self, move_function: Callable, up_msg: msg.BitPattern, down_msg: msg.BitPattern):
        self.up = _Move(move_function, up_msg)
        self.down = _Move(move_function, down_msg)


class _Base(_Actuator):
    def __init__(self, move_function: Callable, cw_msg: msg.BitPattern, ccw_msg: msg.BitPattern):
        self.cw = _Move(move_function, cw_msg)
        self.ccw = _Move(move_function, ccw_msg)


class _LED(_Actuator):
    def __init__(self, move_function: Callable, on_msg: msg.BitPattern, off_msg: msg.BitPattern):
        self.on = _Move(move_function, on_msg)
        self.off = _Move(move_function, off_msg)


class Arm(object):
    """Arm interface"""
    __slots__ = ['dev', 'grippers', 'wrist', 'elbow', 'shoulder', 'base', 'led']

    def __init__(self):
        # Get USB device
        try:
            self.dev = usb.core.find(idVendor=0x1267)
        except usb.core.NoBackendError:
            raise SystemError("The libusb-win32 package is not installed.")
        if not self.dev:
            raise RuntimeError("USB Arm not found. Ensure driver is installed "
                               "and the arm is plugged in and powered on.")
        self.dev.set_configuration()

        # Establish joints
        self.grippers = _EndEffector(self.move, open_msg=msg.GRIPPERS.OPEN, close_msg=msg.GRIPPERS.CLOSE)
        self.wrist = _Joint(self.move, up_msg=msg.WRIST.UP, down_msg=msg.WRIST.DOWN)
        self.elbow = _Joint(self.move, up_msg=msg.ELBOW.UP, down_msg=msg.ELBOW.DOWN)
        self.shoulder = _Joint(self.move, up_msg=msg.SHOULDER.UP, down_msg=msg.SHOULDER.DOWN)
        self.base = _Base(self.move, cw_msg=msg.BASE.CW, ccw_msg=msg.BASE.CCW)
        self.led = _LED(self.move, on_msg=msg.LED.ON, off_msg=msg.LED.OFF)

    def _tell(self, message: msg.BitPattern):
        """Send a USB message to the arm"""
        self.dev.ctrl_transfer(0x40, 6, 0x100, 0, message)

    def stop(self):
        self._tell(msg.STOP)

    def safe_tell(self, fn):
        """
        Send a message to the arm, with a stop
        to ensure that the robot stops in the
        case of an exception
        """
        try:
            fn()
        except Exception:
            self.stop()
            raise

    def move(self, pattern: msg.BitPattern, time=DEFAULT_DURATION):
        """Perform a pattern move with timing and stop"""
        try:
            self._tell(pattern)
            sleep(time)
        finally:
            self.stop()

    def blink(self, count=5):
        """Blink the LED on the arm. By default, five times."""
        for _ in range(count):
            self.led.on(0.5)
            self.led.off(0.5)

    def block_left(self):
        self.grippers.close(1.1)
        self.base.ccw(8.5)
        self.grippers.open()
        self.blink()

    def block_right(self):
        self.grippers.close(1.1)
        self.base.cw(8.5)
        self.grippers.open()
        self.blink()
