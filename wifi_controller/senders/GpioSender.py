import logging
from time import sleep

from wifi_controller.core.Sender import Sender


def press(button):
    print("press", button)
    Sender.sock.sendto(f"press {button}".encode(), (Sender.address[4][0], Sender.myport))


def release(button):
    print("release", button)
    Sender.sock.sendto(f"release {button}".encode(), (Sender.address[4][0], Sender.myport))


def close():
    print("goodbye")
    GpioSender.should_exit = True


class Pin:

    def __init__(self, pin_id) -> None:
        super().__init__()
        self.id = pin_id


class Button:

    def __init__(self, pin, button_id) -> None:
        super().__init__()
        import digitalio
        io = digitalio.DigitalInOut(Pin(pin))
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.UP
        self.io = io
        self.id = button_id

    def is_pressed(self) -> int:
        return 1 if not self.io.value else 0

    def is_released(self) -> int:
        return 1 if self.io.value else 0


class Stick:

    def __init__(self, name, x_channel, y_channel, deadzone, scl=3, sda=2) -> None:
        super().__init__()
        import busio
        import adafruit_ads1x15.ads1015 as ADS
        from adafruit_ads1x15.analog_in import AnalogIn
        i2c = busio.I2C(scl, sda)
        ads = ADS.ADS1015(i2c)
        self.name = name
        self.x_chan = AnalogIn(ads, x_channel)
        self.y_chan = AnalogIn(ads, y_channel)
        self.deadzone = deadzone
        self.middle = 26256 / 2

    def get_value(self):
        x_value = self.x_chan.value
        if x_value > self.middle:
            if x_value - self.middle < self.deadzone:
                x_value = self.middle
        if x_value < self.middle:
            if self.middle - x_value < self.deadzone:
                x_value = self.middle
        y_value = self.y_chan.value
        if y_value > self.middle:
            if y_value - self.middle < self.deadzone:
                y_value = self.middle
        if y_value < self.middle:
            if self.middle - y_value < self.deadzone:
                y_value = self.middle
        return x_value, y_value

    def get_voltage(self):
        return self.x_chan.voltage, self.y_chan.voltage


class GpioSender(Sender):
    should_exit = False

    def __init__(self, group, conf) -> None:
        super().__init__(group)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

        # player_one_button = Button(22, 0)
        # player_two_button = Button(23, 0)

        buttons = []
        for button in conf['buttons']:
            buttons.append(Button(button['pin'], button['value']))

        sticks = []
        for stick in conf['sticks']:
            sticks.append(Stick(stick['name'], stick['x_channel'], stick['y_channel'], stick['deadzone']))

        while not GpioSender.should_exit:
            states = {}
            for button in buttons:
                states[button.id] = button.is_pressed()
            for stick in sticks:
                value = stick.get_value()
                states[stick.name + 'x'] = value[0]
                states[stick.name + 'y'] = value[1]
            logging.info(str(states))
            Sender.sock.sendto(str(states).encode(), (Sender.address[4][0], Sender.myport))
            sleep(0.01)
