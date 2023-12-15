"""
Maplin/OWI USB Robot arm control.

Code derrived from python_usb_robot_arm by orionrobots

Usage:

>>> import usb_arm
>>> arm = usb_arm.Arm()
>>> arm.grippers_open()
>>> arm.block_left()  # WARNING - ARM SHOULD BE ALL THE WAY RIGHT BEFORE TRYING THIS

"""

from usb_arm.usb_signals import BitPattern, MESSAGE as MSG
import usb.core
from time import sleep

DEFAULT_DURATION = 1  # seconds


class _Action:
    def __init__(self, move_fcn, message: BitPattern):
        self._move = move_fcn
        self.message = message

    def __call__(self, time: float = DEFAULT_DURATION):
        self._move(self.message, time)

    def __or__(self, other):
        return _Action(self._move, self.message | other.message)

    def __repr__(self):
        return "<_Action with message:%s>" % self.message

    def __str__(self):
        return self.__repr__()


class Arm:
    """Arm interface"""

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
        self.grippers_open = self.make_action(MSG.GRIPPERS_OPEN)
        self.grippers_close = self.make_action(MSG.GRIPPERS_CLOSE)
        self.wrist_up = self.make_action(MSG.WRIST_UP)
        self.wrist_down = self.make_action(MSG.WRIST_DOWN)
        self.elbow_up = self.make_action(MSG.ELBOW_UP)
        self.elbow_down = self.make_action(MSG.ELBOW_DOWN)
        self.shoulder_up = self.make_action(MSG.SHOULDER_UP)
        self.shoulder_down = self.make_action(MSG.SHOULDER_DOWN)
        self.base_cw = self.make_action(MSG.BASE_CW)
        self.base_ccw = self.make_action(MSG.BASE_CCW)
        self.led_on = self.make_action(MSG.LED_ON)
        self.led_off = self.make_action(MSG.LED_OFF)

    def tell(self, message: BitPattern):
        """Send a USB message to the arm"""
        self.dev.ctrl_transfer(0x40, 6, 0x100, 0, message)

    def stop(self):
        self.tell(MSG.STOP)

    def move(self, pattern: BitPattern, time: float = DEFAULT_DURATION):
        """Perform a pattern move with timing and stop"""
        try:
            self.tell(pattern)
            sleep(time)
        finally:
            self.stop()

    def make_action(self, pattern: BitPattern):
        """Creates _Action object"""
        return _Action(self.move, pattern)

    def blink(self, count=5):
        """Blink the LED on the arm. By default, five times."""
        for _ in range(count):
            self.led_on(0.5)
            self.led_off(0.5)

    def block_left(self):
        self.grippers_close(1.1)
        self.base_ccw(8.5)
        self.grippers_open()
        self.blink()

    def block_right(self):
        self.grippers_close(1.1)
        self.base_cw(8.5)
        self.grippers_open()
        self.blink()
