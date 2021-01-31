from pynput.mouse import Controller as Mouse
from core.Sender import Sender


class DesktopSender(Sender):
    
    middle = None
    mouse = Mouse()

    def __init__(self, group) -> None:
        super().__init__(group)
        print("starting DesktopSender...")
        from pynput import keyboard
        listener = keyboard.Listener(on_press=DesktopSender.on_press, on_release=DesktopSender.on_release)
        listener.start()  # start to listen on a separate thread

        from pynput import mouse
        from screeninfo import get_monitors
        monitor = get_monitors()[0]
        DesktopSender.middle = (monitor.width / 2, monitor.height/ 2)
        DesktopSender.mouse.position = DesktopSender.middle
        listener2 = mouse.Listener(on_move=DesktopSender.on_move, on_click=DesktopSender.on_click)
        listener2.start()

        listener.join()


    @staticmethod
    def on_press(key):
        from pynput import keyboard
        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except Exception as e:
            print(e)
            k = key.name  # other keys
        k = f"press {k}"
        print('Key pressed: ' + k)
        Sender.sock.sendto(k.encode(), (Sender.address[4][0], Sender.myport))

    @staticmethod
    def on_release(key):
        from pynput import keyboard
        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except Exception as e:
            print(e)
            k = key.name  # other keys
        k = f"release {k}"
        print('Key released: ' + k)
        Sender.sock.sendto(k.encode(), (Sender.address[4][0], Sender.myport))

    @staticmethod
    def on_move(x, y):
        if x != DesktopSender.middle[0] and y != DesktopSender.middle[1]:
            print('Pointer moved to {0}'.format((x, y)))
            k = f"moved {x - DesktopSender.middle[0]},{y - DesktopSender.middle[1]}"
            Sender.sock.sendto(k.encode(), (Sender.address[4][0], Sender.myport))
            DesktopSender.mouse.position = DesktopSender.middle

    @staticmethod
    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        k = f"clicked {button.name},{pressed},{x},{y}"
        Sender.sock.sendto(k.encode(), (Sender.address[4][0], Sender.myport))
