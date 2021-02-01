from core.Sender import Sender


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

        a_button.when_pressed = lambda: Sender.sock.sendto(f"press 13".encode(),
                                                           (Sender.address[4][0], Sender.myport))
        a_button.when_released = lambda: Sender.sock.sendto(f"release 13".encode(),
                                                            (Sender.address[4][0], Sender.myport))

        x_button.when_pressed = lambda: Sender.sock.sendto(f"press 14".encode(),
                                                           (Sender.address[4][0], Sender.myport))
        x_button.when_released = lambda: Sender.sock.sendto(f"release 14".encode(),
                                                            (Sender.address[4][0], Sender.myport))

        b_button.when_pressed = lambda: Sender.sock.sendto(f"press 15".encode(),
                                                           (Sender.address[4][0], Sender.myport))
        b_button.when_released = lambda: Sender.sock.sendto(f"release 15".encode(),
                                                            (Sender.address[4][0], Sender.myport))

        y_button.when_pressed = lambda: Sender.sock.sendto(f"press 16".encode(),
                                                           (Sender.address[4][0], Sender.myport))
        y_button.when_released = lambda: Sender.sock.sendto(f"release 16".encode(),
                                                            (Sender.address[4][0], Sender.myport))

        while True:
            pass
