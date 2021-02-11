import logging
import json
from time import time

from wifi_controller.core.Receiver import Receiver
from wifi_controller.core.EventAuditor import audit_event


def translate(value, left_min, left_max, right_min, right_max):
    # Figure out how 'wide' each range is
    left_span = left_max - left_min
    right_span = right_max - right_min

    # Convert the left range into a 0-1 range (float)
    value_scaled = float(value - left_min) / float(left_span)

    # Convert the 0-1 range into a value in the right range.
    return right_min + (value_scaled * right_span)


class GamepadReceiver(Receiver):

    def __init__(self, group, audit) -> None:
        super().__init__(group)
        self.joys = {}
        self.audit = audit

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
                    # TODO: should I export this to conf?
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
                state['Lx'] = translate(state['Lx'], 0, 26256, -1, 1)
                state['Ly'] = -1 * translate(state['Ly'], 0, 26256, -1, 1)
            if 'Rx' in state:
                state['Rx'] = translate(state['Rx'], 0, 26256, -1, 1)
                state['Ry'] = -1 * translate(state['Ry'], 0, 26256, -1, 1)
            con.playMoment(state)
            if self.audit:
                audit_event('pc.txt', state | {'time': time()})
