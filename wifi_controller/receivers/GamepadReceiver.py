import logging
from wifi_controller.core.Receiver import Receiver


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
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
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
                logging.info(f"New Connection: {sender}")
                j = pyvjoy.VJoyDevice(len(self.joys) + 1)
                j.set_axis(pyvjoy.HID_USAGE_X, int(middle))
                j.set_axis(pyvjoy.HID_USAGE_Y, int(middle))
                self.joys[sender] = j  # TODO: Think about when to "close" connection
            if data == "goodbye":
                logging.info("bye bye")
                del self.joys[sender]
                continue
            event, actions = data.split(" ")  # TODO: change to pattern matching with python3.10
            if event == "press" or event == "release":
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
                    logging.info(e)
                    continue
                except ValueError as e:
                    logging.info(e)
                    continue
                j.set_button(key, event)
            elif event == "moved":
                x, y = actions.split(',')
                x = float(x)
                y = float(y)
                if x <= -400:  # left
                    j.set_button(15, 1)
                elif x >= 400:  # right
                    j.set_button(16, 1)
                else:
                    j.set_button(15, 0)
                    j.set_button(16, 0)
                if y <= -400:  # up
                    j.set_button(13, 1)
                elif y >= 400:  # down
                    j.set_button(14, 1)
                else:
                    j.set_button(13, 0)
                    j.set_button(14, 0)
                # pos = (int(x.split('.')[0]), int(y.split('.')[0]))
                # pos = (self.translate(pos[0], -800, 840, min, max), self.translate(pos[1], -800, 840, min, max))
                # # dx = pos[0] - last_pos[0]
                # # dy = pos[1] - last_pos[1]
                # logging.info(pos)
                # j.set_axis(pyvjoy.HID_USAGE_X, int(middle + (int(pos[0]) * 100)))
                # j.set_axis(pyvjoy.HID_USAGE_Y, int(middle + (int(pos[1]) * 100)))

                # last_pos = pos
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
