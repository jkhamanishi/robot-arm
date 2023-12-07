import usb_arm
from controller import ControllerApp

if __name__ == "__main__":
    # Establish connection
    arm = usb_arm.Arm()

    # Test connection
    arm.blink()

    # Connect to controller
    app = ControllerApp(arm)
    app.run(host="0.0.0.0", port=5000, debug=True)

