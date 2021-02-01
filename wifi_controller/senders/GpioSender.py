from core.Sender import Sender


def press(button):
    print("press", button)
    Sender.sock.sendto(f"press {button}".encode(), (Sender.address[4][0], Sender.myport))


def release(button):
    print("release", button)
    Sender.sock.sendto(f"release {button}".encode(), (Sender.address[4][0], Sender.myport))


class GpioSender(Sender):
    def __init__(self, group) -> None:
        super().__init__(group)
        from gpiozero import Button
        a_button = Button(12)
        x_button = Button(16)
        b_button = Button(6)
        y_button = Button(13)
        start_button = Button(26)
        select_button = Button(20)
        player_one_button = Button(22)
        player_two_button = Button(23)

        a_button.when_pressed = lambda: press(1)
        a_button.when_released = lambda: release(1)

        x_button.when_pressed = lambda: press(2)
        x_button.when_released = lambda: release(2)

        b_button.when_pressed = lambda: press(3)
        b_button.when_released = lambda: release(3)

        y_button.when_pressed = lambda: press(4)
        y_button.when_released = lambda: release(4)

        while True:
            pass
