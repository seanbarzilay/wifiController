from pynput.keyboard import Key, Controller as Keyboard
from pynput.mouse import Button, Controller as Mouse

from Receiver import Receiver


class KeyboardReceiver(Receiver):

    def __init__(self, group) -> None:
        super().__init__(group)
        self.keyboard = Keyboard()
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
                self.keyboard[event](key)
                
            elif event == "moved":
                x, y = actions.split(',')
                pos = (int(x.split('.')[0]), int(y.split('.')[0]))
                self.mouse.position = pos
            elif event == "clicked":
                button, pressed, x, y = actions.split(',')
                if pressed == 'True':
                    self.mouse.press(Button[button])
                else:
                    self.mouse.release(Button[button])
