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

    def __init__(self, pin, pin_id) -> None:
        super().__init__()
        import digitalio
        io = digitalio.DigitalInOut(Pin(pin))
        io.direction = digitalio.Direction.INPUT
        io.pull = digitalio.Pull.UP
        self.io = io
        self.id = pin_id

    def is_pressed(self) -> int:
        return 1 if not self.io.value else 0

    def is_released(self) -> int:
        return 1 if self.io.value else 0


class Stick:

    def __init__(self, pin, deadzone, scl=3, sda=2) -> None:
        super().__init__()
        import busio
        import adafruit_ads1x15.ads1015 as ADS
        from adafruit_ads1x15.analog_in import AnalogIn
        i2c = busio.I2C(scl, sda)
        ads = ADS.ADS1015(i2c)
        self.chan = AnalogIn(ads, pin)
        self.deadzone = deadzone
        self.middle = 26256 / 2

    def get_value(self):
        value = self.chan.value
        if value > self.middle:
            print("bigger: ", (value - self.middle))
            if value - self.middle < self.deadzone:
                value = self.middle
        if value < self.middle:
            print("smaller: ", (self.middle - value))
            if self.middle - value < self.deadzone:
                value = self.middle
        return value

    def get_voltage(self):
        return self.chan.voltage


class GpioSender(Sender):
    should_exit = False

    def __init__(self, group) -> None:
        super().__init__(group)

        a_button = Button(12, 2)
        x_button = Button(16, 4)
        b_button = Button(6, 1)
        y_button = Button(13, 3)
        start_button = Button(26, 9)
        select_button = Button(20, 10)
        player_one_button = Button(22, 0)
        player_two_button = Button(23, 0)

        stick_y = Stick(0, 700)
        stick_x = Stick(1, 700)

        buttons = [
            a_button,
            x_button,
            b_button,
            y_button,
            start_button,
            select_button,
            player_one_button,
            player_two_button
        ]

        while not GpioSender.should_exit:
            states = {}
            for button in buttons:
                states[button.id] = button.is_pressed()
            states['x'] = stick_x.get_value()
            states['y'] = stick_y.get_value()
            print(states)
            sleep(0.01)
