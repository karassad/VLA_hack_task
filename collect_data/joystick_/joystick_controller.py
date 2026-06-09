import evdev
from evdev import InputDevice, ecodes


class JoystickController:
    def __init__(self, 
                 device_path='/dev/input/by-id/usb-Logitech_Logitech_Dual_Action-event-joystick'
                                   ):
        self.device = InputDevice(device_path)
        self.axes = {0: 128, 1: 128, 2: 128, 5: 128}
        self.gripper_state = False
        self.wrist_roll_angle = 0.0

    def get_action(self):
        wrist_step = 0.05
        self.wrist_roll_angle= 0.0
        try:
            for event in self.device.read():
                if event.type == ecodes.EV_ABS:
                    self.axes[event.code] = event.value

                elif event.type == ecodes.EV_KEY and event.value == 1:
                    if event.code == 289:  #Захват 2
                        self.gripper_state = not self.gripper_state
                    elif event.code == 288:  #поворот влево 1
                        self.wrist_roll_angle -= wrist_step
                    elif event.code == 290:  #поворот вправо 3
                        self.wrist_roll_angle += wrist_step
        except BlockingIOError:
            pass

        def norm(val, deadzone=10):

            diff = val - 128
            if abs(diff) < deadzone:
                return 0.0
            return (val - 128) / 128.0

        # [shoulder_pan, shoulder_lift, elbow_flex, wrist_flex, wrist_roll, gripper]
        speed = 0.05

        dq = [
            norm(self.axes[0]) * speed,
            norm(self.axes[1]) * speed,
            norm(self.axes[2]) * speed,
            norm(self.axes[5]) * speed,
            self.wrist_roll_angle,
            1.2 if self.gripper_state else 0.0
        ]
        return dq