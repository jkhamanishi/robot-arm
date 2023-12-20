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
        return usb_arm.usb_signals.MESSAGE.STOP
    else:
        return usb_arm.usb_signals.MESSAGE[f"{actuator}_{direction}"]


def create_message(move_list) -> usb_arm.usb_signals.BitPattern:
    message = get_pattern("STOP")
    for action in move_list:
        message = message | get_pattern(*action)
    return message


class ControllerApp(Flask):
    def __init__(self, arm: usb_arm.Arm = None):
        super().__init__(__name__, static_url_path="/static")
        app = self
        self.move_list = []

        @app.route('/')
        def index():
            if arm is not None:
                arm.stop()
                self.move_list.clear()
            return render_template('index.html')

        def update_move_list(actuator, direction, toggle):
            button_action = [actuator, direction]
            if actuator == "STOP":
                keep_led_on = ["LED", "ON"] in self.move_list and direction != "ALL"
                self.move_list.clear()
                if keep_led_on:
                    self.move_list.append(["LED", "ON"])
            elif toggle == "ON":
                self.move_list.append(button_action)
            elif toggle == "OFF" and button_action in self.move_list:
                self.move_list.remove(button_action)

        @app.route('/move', methods=['POST'])
        def move():
            actuator = request.form['actuator']
            direction = request.form['direction']
            toggle = request.form['toggle']
            update_move_list(actuator, direction, toggle)
            message = create_message(self.move_list)
            if arm is not None:
                arm.tell(message)
            else:
                app.logger.debug(self.move_list)
                app.logger.debug(message)
            return Response()


if __name__ == "__main__":
    test_app = ControllerApp()
    test_app.run(host="0.0.0.0", port=5000, debug=True)
