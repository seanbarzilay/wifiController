from pynput import keyboard, mouse

import struct
import socket
import time


class Sender:
    sock = None
    myport = 8123
    address = None

    def __init__(self, group) -> None:
        ttl = 2  # Increase to reach other networks
        address = socket.getaddrinfo(group, None)[0]

        s = socket.socket(address[0], socket.SOCK_DGRAM)

        # Set Time-to-live (optional)
        ttl_bin = struct.pack('@i', ttl)
        if address[0] == socket.AF_INET:  # IPv4
            print("test2")
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
            print("test3")
        else:
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

        Sender.sock = s
        Sender.address = address
        listener = keyboard.Listener(on_press=Sender.on_press, on_release=Sender.on_release)
        listener.start()  # start to listen on a separate thread

        listener2 = mouse.Listener(
            on_move=Sender.on_move,
            on_click=Sender.on_click)
        listener2.start()

        listener.join()
        print("start listen")

    @staticmethod
    def on_press(key):
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
        print('Pointer moved to {0}'.format((x, y)))
        k = f"moved {x},{y}"
        Sender.sock.sendto(k.encode(), (Sender.address[4][0], Sender.myport))

    @staticmethod
    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        k = f"clicked {button.name},{pressed},{x},{y}"
        Sender.sock.sendto(k.encode(), (Sender.address[4][0], Sender.myport))
