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
            print("bigger: " + (value - self.middle))
            if value - self.middle < self.deadzone:
                value = self.middle
        if value < self.middle:
            print("smaller: " + (self.middle - value))
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

        stick_y = Stick(0)
        stick_x = Stick(1)

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

        while True:
            states = {}
            for button in buttons:
                states[button.id] = button.is_pressed()
            print(states)
            print(f"stick_y value: {stick_y.get_value()}")
            # print(f"stick_y voltage: {stick_y.get_voltage()}")
            print(f"stick_x value: {stick_x.get_value()}")
            # print(f"stick_x voltage: {stick_x.get_voltage()}")
            sleep(1)

        # from gpiozero import Button
        # import RPi.GPIO as gpio
        # from smbus import SMBus
        #
        # BOUNCE_TIME = 0.01  # Debounce time in seconds
        #
        # bus = SMBus(1)
        # gpio.setwarnings(False)
        # gpio.setmode(gpio.BCM)
        #
        # MOUSE_SENSITIVITY = 4  # 0-10
        # MOUSE_DEADZONE = 40  # Values under this are zeroed
        # ###################################### ADS1015 microdriver #################################
        # # Register and other configuration values:
        # ADS1x15_DEFAULT_ADDRESS = 0x48
        # ADS1x15_POINTER_CONVERSION = 0x00
        # ADS1x15_POINTER_CONFIG = 0x01
        #
        # ADS1015_REG_CONFIG_CQUE_NONE = 0x0003  # Disable the comparator and put ALERT/RDY in high state (default)
        # ADS1015_REG_CONFIG_CLAT_NONLAT = 0x0000  # Non-latching comparator (default)
        # ADS1015_REG_CONFIG_CPOL_ACTVLOW = 0x0000  # ALERT/RDY pin is low when active (default)
        # ADS1015_REG_CONFIG_CMODE_TRAD = 0x0000  # Traditional comparator with hysteresis (default)
        # ADS1015_REG_CONFIG_DR_1600SPS = 0x0080  # 1600 samples per second (default)
        # ADS1015_REG_CONFIG_MODE_SINGLE = 0x0100  # Power-down single-shot mode (default)
        # ADS1015_REG_CONFIG_GAIN_ONE = 0x0200  # gain of 1
        #
        # ADS1015_REG_CONFIG_MUX_SINGLE_0 = 0x4000  # channel 0
        # ADS1015_REG_CONFIG_MUX_SINGLE_1 = 0x5000  # channel 1
        # ADS1015_REG_CONFIG_MUX_SINGLE_2 = 0x6000  # channel 2
        # ADS1015_REG_CONFIG_MUX_SINGLE_3 = 0x7000  # channel 3
        #
        # ADS1015_REG_CONFIG_OS_SINGLE = 0x8000  # start a single conversion
        #
        # ADS1015_REG_CONFIG_CHANNELS = (ADS1015_REG_CONFIG_MUX_SINGLE_0, ADS1015_REG_CONFIG_MUX_SINGLE_1,
        #                                ADS1015_REG_CONFIG_MUX_SINGLE_2, ADS1015_REG_CONFIG_MUX_SINGLE_3)
        #
        #
        #
        # def ads_read(channel):
        #     # configdata = bus.read_i2c_block_data(ADS1x15_DEFAULT_ADDRESS, ADS1x15_POINTER_CONFIG, 2)
        #     # print("Getting config byte = 0x%02X%02X" % (configdata[0], configdata[1]))
        #
        #     configword = ADS1015_REG_CONFIG_CQUE_NONE | ADS1015_REG_CONFIG_CLAT_NONLAT | ADS1015_REG_CONFIG_CPOL_ACTVLOW | ADS1015_REG_CONFIG_CMODE_TRAD | ADS1015_REG_CONFIG_DR_1600SPS | ADS1015_REG_CONFIG_MODE_SINGLE | ADS1015_REG_CONFIG_GAIN_ONE | \
        #                  ADS1015_REG_CONFIG_CHANNELS[channel] | ADS1015_REG_CONFIG_OS_SINGLE
        #     configdata = [configword >> 8, configword & 0xFF]
        #
        #     # print("Setting config byte = 0x%02X%02X" % (configdata[0], configdata[1]))
        #     bus.write_i2c_block_data(ADS1x15_DEFAULT_ADDRESS, ADS1x15_POINTER_CONFIG, configdata)
        #
        #     configdata = bus.read_i2c_block_data(ADS1x15_DEFAULT_ADDRESS, ADS1x15_POINTER_CONFIG, 2)
        #     # print("Getting config byte = 0x%02X%02X" % (configdata[0], configdata[1]))
        #
        #     while True:
        #         try:
        #             configdata = bus.read_i2c_block_data(ADS1x15_DEFAULT_ADDRESS, ADS1x15_POINTER_CONFIG, 2)
        #             # print("Getting config byte = 0x%02X%02X" % (configdata[0], configdata[1]))
        #             if (configdata[0] & 0x80):
        #                 break
        #         except:
        #             pass
        #     # read data out!
        #     analogdata = bus.read_i2c_block_data(ADS1x15_DEFAULT_ADDRESS, ADS1x15_POINTER_CONVERSION, 2)
        #     # print(analogdata),
        #     retval = (analogdata[0] << 8) | analogdata[1]
        #     retval /= 16
        #     # print("-> %d" %retval)
        #     return retval
        #
        # a_button = Button(12)
        # x_button = Button(16)
        # b_button = Button(6)
        # y_button = Button(13)
        # start_button = Button(26)
        # select_button = Button(20)
        # player_one_button = Button(22)
        # player_two_button = Button(23)
        #
        # player_one_button.when_pressed = lambda: close()
        #
        # a_button.when_pressed = lambda: press(2)
        # a_button.when_released = lambda: release(2)
        #
        # x_button.when_pressed = lambda: press(4)
        # x_button.when_released = lambda: release(4)
        #
        # b_button.when_pressed = lambda: press(1)
        # b_button.when_released = lambda: release(1)
        #
        # y_button.when_pressed = lambda: press(3)
        # y_button.when_released = lambda: release(3)
        #
        # start_button.when_pressed = lambda: press(9)
        # start_button.when_released = lambda: release(9)
        #
        # select_button.when_pressed = lambda: press(10)
        # select_button.when_released = lambda: release(10)
        #
        # while True:
        #     if GpioSender.should_exit:
        #         Sender.sock.sendto("goodbye".encode(), (Sender.address[4][0], Sender.myport))
        #         break
        #     try:
        #         y = 800 - ads_read(0)
        #         x = ads_read(1) - 800
        #     except IOError:
        #         continue
        #     if abs(x) < MOUSE_DEADZONE:
        #         x = 0
        #     if abs(y) < MOUSE_DEADZONE:
        #         y = 0
        #     # x = x >> (10 - MOUSE_SENSITIVITY)
        #     # y = y >> (10 - MOUSE_SENSITIVITY)
        #     y = -y
        #     Sender.sock.sendto(f"moved {x},{y}".encode(), (Sender.address[4][0], Sender.myport))
        #     sleep(0.01)
