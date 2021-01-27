from pynput import keyboard

import struct
import socket


class Sender:
    sock = None
    myport = 8123
    addrinfo = None

    def __init__(self) -> None:
        mygroup_4 = '225.0.0.250'
        myttl = 1  # Increase to reach other networks
        addrinfo = socket.getaddrinfo(mygroup_4, None)[0]

        s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

        # Set Time-to-live (optional)
        ttl_bin = struct.pack('@i', myttl)
        if addrinfo[0] == socket.AF_INET:  # IPv4
            s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
        else:
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)

        Sender.sock = s
        Sender.addrinfo = addrinfo
        listener = keyboard.Listener(on_press=Sender.on_press)
        listener.start()  # start to listen on a separate thread
        listener.join()

    @staticmethod
    def on_press(key):
        if key == keyboard.Key.esc:
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        print('Key pressed: ' + k)
        Sender.sock.sendto(k.encode(), (Sender.addrinfo[4][0], Sender.myport))
        return True
