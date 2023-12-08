"""
Maplin/OWI USB Robot arm control via Flask webpage.
Code derrived from python_usb_robot_arm by orionrobots

Usage:

>>> from controller import ControllerApp
>>> app = ControllerApp()
>>> app.run(host="0.0.0.0", port=5000)

"""

import usb_arm
from flask import Flask, Response, request, render_template


def get_pattern(actuator: str, direction: str = None) -> usb_arm.usb_signals.BitPattern:
    if actuator == "STOP":
        return usb_arm.usb_signals.STOP
    else:
        return getattr(getattr(usb_arm.usb_signals, actuator), direction)


class ControllerApp(Flask):
    def __init__(self, arm: usb_arm.Arm = None):
        super().__init__(__name__)
        move_list = []

        @self.route('/')
        def index():
            if arm is not None:
                arm.stop()
                move_list.clear()
            return render_template('index.html')

        @self.route('/move', methods=['POST'])
        def move():
            actuator = request.form['actuator']
            direction = request.form['direction']
            button_action = [actuator, direction]
            toggle = request.form['toggle']
            if actuator == "STOP":
                keep_led_on = ["LED", "ON"] in move_list and direction != "ALL"
                move_list.clear()
                if keep_led_on:
                    move_list.append(["LED", "ON"])
            elif toggle == "ON":
                move_list.append(button_action)
            elif toggle == "OFF" and button_action in move_list:
                move_list.remove(button_action)
            self.logger.info(move_list)
            message = get_pattern("STOP")
            for action in move_list:
                message = message | get_pattern(*action)
            if arm is not None:
                arm.tell(message)
            else:
                self.logger.debug(message)
            return Response()


if __name__ == "__main__":
    test_app = ControllerApp()
    test_app.run(host="0.0.0.0", port=5000, debug=True)
