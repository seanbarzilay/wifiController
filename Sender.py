from pynput import keyboard, mouse

import struct
import socket
import time


class Sender:
    sock = None
    myport = 8123
    addrinfo = None

    def __init__(self) -> None:
        print("test")
        mygroup_4 = '225.0.0.250'
        myttl = 2  # Increase to reach other networks
        addrinfo = socket.getaddrinfo(mygroup_4, None)[0]

        s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

        # Set Time-to-live (optional)
        ttl_bin = struct.pack('@i', myttl)
        if addrinfo[0] == socket.AF_INET:  # IPv4
            print("test2")
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
            print("test3")
        else:
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

        Sender.sock = s
        Sender.addrinfo = addrinfo
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
        except:
            k = key.name  # other keys
        k = f"press {k}"
        print('Key pressed: ' + k)
        Sender.sock.sendto(k.encode(), (Sender.addrinfo[4][0], Sender.myport))

    @staticmethod
    def on_release(key):
        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k= key.char  # single-char keys
        except:
            k = key.name  # other keys
        k = f"release {k}"
        print('Key released: ' + k)
        Sender.sock.sendto(k.encode(), (Sender.addrinfo[4][0], Sender.myport))

    @staticmethod
    def on_move(x, y):
        print('Pointer moved to {0}'.format((x, y)))
        k = f"moved {x},{y}"
        Sender.sock.sendto(k.encode(), (Sender.addrinfo[4][0], Sender.myport))

    @staticmethod
    def on_click(x, y, button, pressed):
        print('{0} at {1}'.format('Pressed' if pressed else 'Released', (x, y)))
        k = f"clicked {button.name},{pressed},{x},{y}"
        Sender.sock.sendto(k.encode(), (Sender.addrinfo[4][0], Sender.myport))
