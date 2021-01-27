#!/usr/bin/env python
#
# Send/receive UDP multicast packets.
# Requires that your OS kernel supports IP multicast.
#
# Usage:
#   mcast -s (sender, IPv4)
#   mcast -s -6 (sender, IPv6)
#   mcast    (receivers, IPv4)
#   mcast  -6  (receivers, IPv6)
from Sender import Sender

MYPORT = 8123
MYGROUP_4 = '225.0.0.250'
MYGROUP_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'
MYTTL = 1  # Increase to reach other networks

import struct
import socket
import sys

from pynput import keyboard
from pynput.keyboard import Key, Controller
from pynput.mouse import Button, Controller as Mouse


def main():
    group = MYGROUP_6 if "-6" in sys.argv[1:] else MYGROUP_4

    if "-s" in sys.argv[1:]:
        sender(group)
    else:
        receiver(group)


def on_press(key):
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['1', '2', 'left', 'right']:  # keys of interest
        # self.keys.append(k)  # store it in global-like variable
        print('Key pressed: ' + k)
        return False  # stop listener; remove this if want more keys


def sender(group):
    Sender()
    # addrinfo = socket.getaddrinfo(group, None)[0]
    #
    # s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
    #
    # # Set Time-to-live (optional)
    # ttl_bin = struct.pack('@i', MYTTL)
    # if addrinfo[0] == socket.AF_INET:  # IPv4
    #     s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl_bin)
    # else:
    #     s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_MULTICAST_HOPS, ttl_bin)
    #
    # listener = keyboard.Listener(on_press=on_press)
    # listener.start()  # start to listen on a separate thread
    # listener.join()
    #
    # while True:
    #     data = repr(time.time())
    #     s.sendto((data + '\0').encode(), (addrinfo[4][0], MYPORT))
    #     time.sleep(1)

def read_data(s):
    data, sender = s.recvfrom(1500)
    while data[-1:] == '\0':
        data = data[:-1]  # Strip trailing \0's
    print(str(sender) + '  ' + repr(data))
    data = data.decode()
    return data, sender

def receiver(group):
    import pyvjoy
    keys = Controller()
    mouse = Mouse()
    # Look up multicast group address in name server and find out IP version
    addrinfo = socket.getaddrinfo(group, None)[0]

    # Create a socket
    s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)

    # Allow multiple copies of this program on one machine
    # (not strictly needed)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind it to the port
    s.bind(('', MYPORT))

    group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
    if addrinfo[0] == socket.AF_INET:  # IPv4
        mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
        s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    else:
        mreq = group_bin + struct.pack('@I', 0)
        s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)

    j = pyvjoy.VJoyDevice(1)

    # Loop, printing any data we receive
    lastPos = (0, 0)
    mouse.position = lastPos
    middle = 0x8000 / 2
    j.set_axis(pyvjoy.HID_USAGE_X, int(middle))
    j.set_axis(pyvjoy.HID_USAGE_Y, int(middle))
    while True:
        data, sender = read_data(s)
        event, actions = data.split(" ")  # TODO: change to pattern matching with python3.10
        if event == "press" or event == "release":
            if len(actions) > 1:
                key = Key[actions]
            else:
                key = actions
            event = 1 if event == "press" else 0
            if key == Key.up:
                key = 13
            if key == Key.down:
                key = 14
            if key == Key.left:
                key = 15
            if key == Key.right:
                key = 16
            else:
                key = int(key)
            j.set_button(key, event)
        elif event == "moved":
            x, y = actions.split(',')
            pos = (int(x), int(y))
            dx = pos[0] - lastPos[0]
            dy = pos[1] - lastPos[1]
            j.set_axis(pyvjoy.HID_USAGE_X, int(middle + int(str(int(dx) * 100), 16)))
            j.set_axis(pyvjoy.HID_USAGE_Y, int(middle + int(str(int(dy) * 100), 16)))
            # if (lastPos[1] - lastPos[1]) < 0:
            #     j.set_axis(pyvjoy.HID_USAGE_Y, 0x1)
            # else:
            #     j.set_axis(pyvjoy.HID_USAGE_Y, 0x8000)
            lastPos = pos
        elif event == "clicked":
            button, pressed, x, y = actions.split(',')
            # mouse.position = (int(x), int(y))
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


if __name__ == '__main__':
    main()
