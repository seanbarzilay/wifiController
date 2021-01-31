import math

from pynput.keyboard import Key, Controller as Keyboard
from pynput.mouse import Button, Controller as Mouse

from wifi_controller.core.Receiver import Receiver


class KeyboardReceiver(Receiver):

    def __init__(self, group) -> None:
        super().__init__(group)
        self.keyboard = Keyboard()
        self.actions = {
            'press': self.keyboard.press,
            'release': self.keyboard.release
        }
        self.mouse = Mouse()

    def start(self):
        while True:  # TODO Remove infinite loop
            data, sender = Receiver.read_data()
            event, actions = data.split(" ")  # TODO: change to pattern matching with python3.10
            if event == "press" or event == "release":
                if len(actions) > 1:
                    key = Key[actions]
                else:
                    key = actions
                self.actions[event](key)
                
            elif event == "moved":
                x, y = actions.split(',')
                pos = (int(math.ceil(float(x))), int(math.ceil(float(y))))
                self.mouse.move(pos[0], pos[1])
            elif event == "clicked":
                button, pressed, x, y = actions.split(',')
                if pressed == 'True':
                    self.mouse.press(Button[button])
                else:
                    self.mouse.release(Button[button])
