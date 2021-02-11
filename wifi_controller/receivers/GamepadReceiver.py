import logging
import json
from time import time

from wifi_controller.core.Receiver import Receiver
from wifi_controller.core.EventAuditor import audit_event


class GamepadReceiver(Receiver):

    def __init__(self, group, audit) -> None:
        super().__init__(group)
        self.joys = {}
        self.audit = audit

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def start(self):
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        from gamepyd import wPad, c_int, c_bool, c_short, c_byte
        while True:
            data, sender = Receiver.read_data()
            if sender in self.joys:
                con = self.joys[sender]
            else:
                con = wPad()
                self.joys[sender] = con
                con._buttons = {
                    # key button name is mapped to list of label,type,value(for on)
                    'UP': ["Dpad", c_int, 1],
                    'DOWN': ["Dpad", c_int, 2],
                    'LEFT': ["Dpad", c_int, 4],
                    'RIGHT': ["Dpad", c_int, 8],
                    'START': ["BtnStart", c_bool, 1],
                    'SELECT': ["BtnBack", c_bool, 1],
                    'L3': ["BtnThumbL", c_bool, 1],
                    'R3': ["BtnThumbR", c_bool, 1],
                    'LB': ["BtnX", c_bool, 1],
                    'RB': ["BtnX", c_bool, 1],
                    'A': ["BtnA", c_bool, 1],
                    'B': ["BtnB", c_bool, 1],
                    'X': ["BtnX", c_bool, 1],
                    'Y': ["BtnY", c_bool, 1],
                    'Lx': ["AxisLx", c_short, 32767],
                    'Ly': ["AxisLy", c_short, 32767],
                    'Rx': ["AxisRx", c_short, 32767],
                    'Ry': ["AxisRy", c_short, 32767],
                    'LT': ["TriggerL", c_byte, 255],
                    'RT': ["TriggerR", c_byte, 255]
                }
            logging.info(data)
            state = json.loads(data.replace("'", '"'))
            if 'Lx' in state:
                state['Lx'] = self.translate(state['Lx'], 0, 26256, -1, 1)
                state['Ly'] = -1 * self.translate(state['Ly'], 0, 26256, -1, 1)
            if 'Rx' in state:
                state['Rx'] = self.translate(state['Rx'], 0, 26256, -1, 1)
                state['Ry'] = -1 * self.translate(state['Ry'], 0, 26256, -1, 1)
            con.playMoment(state)
            if self.audit:
                audit_event('pc.txt', state | {'time': time()})
