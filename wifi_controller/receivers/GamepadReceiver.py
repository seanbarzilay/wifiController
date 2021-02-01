from wifi_controller.core.Receiver import Receiver
from pynput.keyboard import Key


class GamepadReceiver(Receiver):

    def __init__(self, group) -> None:
        super().__init__(group)
        self.joys = {}

    def translate(self, value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin

        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)

        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)

    def start(self):
        import pyvjoy
        middle = 0x8000 / 2
        min = -800
        max = 840
        last_pos = (0, 0)
        while True:  # TODO Remove infinite loop
            data, sender = Receiver.read_data()
            if sender in self.joys:
                j = self.joys[sender]
            else:
                print(f"New Connection: {sender}")
                j = pyvjoy.VJoyDevice(len(self.joys) + 1)
                j.set_axis(pyvjoy.HID_USAGE_X, int(middle))
                j.set_axis(pyvjoy.HID_USAGE_Y, int(middle))
                self.joys[sender] = j  # TODO: Think about when to "close" connection
            event, actions = data.split(" ")  # TODO: change to pattern matching with python3.10
            if event == "goodbye":
                del self.joys[sender]
            elif event == "press" or event == "release":
                # if len(actions) > 1:
                #     key = Key[actions]
                # else:
                key = actions
                event = 1 if event == "press" else 0
                # if key == Key.up:
                #     key = 13
                # if key == Key.down:
                #     key = 14
                # if key == Key.left:
                #     key = 15
                # if key == Key.right:
                #     key = 16
                # else:
                try:
                    key = int(key)
                    if key == 0:
                        continue
                except TypeError as e:
                    print(e)
                    continue
                except ValueError as e:
                    print(e)
                    continue
                j.set_button(key, event)
            elif event == "moved":
                x, y = actions.split(',')
                pos = (int(x.split('.')[0]), int(y.split('.')[0]))
                # pos = (self.translate(pos[0], -800, 840, min, max), self.translate(pos[1], -800, 840, min, max))
                # dx = pos[0] - last_pos[0]
                # dy = pos[1] - last_pos[1]
                print(pos)
                j.set_axis(pyvjoy.HID_USAGE_X, int(pos[0]))
                j.set_axis(pyvjoy.HID_USAGE_Y, int(pos[1]))

                last_pos = pos
            elif event == "clicked":
                button, pressed, x, y = actions.split(',')
                if pressed == "True":
                    if button == 'left':
                        j.set_button(7, 1)
                    else:
                        j.set_button(8, 1)
                else:
                    if button == 'left':
                        j.set_button(7, 0)
                    else:
                        j.set_button(8, 0)
