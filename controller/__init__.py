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

move_map = {
    "GripsClose": None,
    "CloseGrips": None,
    "GripsOpen": None,
    "OpenGrips": None,
    "Stop": None,
    "WristUp": None,
    "WristDown": None,
    "ElbowUp": None,
    "ElbowDown": None,
    "ShoulderUp": None,
    "ShoulderDown": None,
    "BaseClockWise": None,
    "BaseCtrClockWise": None,
    "LedOn": None
}


class ControllerApp(Flask):
    def __init__(self, arm: usb_arm.Arm = None):
        super().__init__(__name__)
        move_list = []

        @self.route('/')
        def index():
            return render_template('index.html')

        @self.route('/move', methods=['POST'])
        def move():
            action = request.form['action']
            toggle = request.form['toggle']
            if toggle == "on":
                move_list.append(action)
            elif toggle == "off":
                move_list.remove(action)
            # arm.move(pattern)
            return Response()


if __name__ == "__main__":
    test_app = ControllerApp()
    test_app.run(host="0.0.0.0", port=5000, debug=True)
