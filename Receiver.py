import socket
import struct

from pynput.keyboard import Key


class Receiver:
    sock = None
    port = 8123
    address = None
    joy = None
    joys = {}

    def __init__(self, group) -> None:
        import pyvjoy
        Receiver.address = socket.getaddrinfo(group, None)[0]

        s = socket.socket(Receiver.address[0], socket.SOCK_DGRAM)
        # Allow multiple copies of this program on one machine
        # (not strictly needed)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', Receiver.port))
        group_bin = socket.inet_pton(Receiver.address[0], Receiver.address[4][0])
        # Join group
        if Receiver.address[0] == socket.AF_INET:  # IPv4
            mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        else:
            mreq = group_bin + struct.pack('@I', 0)
            s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
        # j = pyvjoy.VJoyDevice(1)
        Receiver.sock = s
        # Receiver.joy = j
        last_pos = (0, 0)
        middle = 0x8000 / 2

        while True:  # TODO Remove infinite loop
            data, sender = Receiver.read_data()
            if sender in Receiver.joys:
                j = Receiver.joys[sender]
            else:
                print(f"New Connection: {sender}")
                j = pyvjoy.VJoyDevice(len(Receiver.joys) + 1)
                j.set_axis(pyvjoy.HID_USAGE_X, int(middle))
                j.set_axis(pyvjoy.HID_USAGE_Y, int(middle))
                Receiver.joys[sender] = j  # TODO: Think about when to "close" connection
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
                    try:
                        key = int(key)
                        if key == 0:
                            continue
                    except TypeError as e:
                        print(e)
                        continue
                    except ValueError as e:
                        print(e)
                        continue
                j.set_button(key, event)
            elif event == "moved":
                x, y = actions.split(',')
                pos = (int(x.split('.')[0]), int(y.split('.')[0]))
                dx = pos[0] - last_pos[0]
                dy = pos[1] - last_pos[1]
                j.set_axis(pyvjoy.HID_USAGE_X, int(middle + int(str(int(dx) * 100), 16)))
                j.set_axis(pyvjoy.HID_USAGE_Y, int(middle + int(str(int(dy) * 100), 16)))

                last_pos = pos
            elif event == "clicked":
                button, pressed, x, y = actions.split(',')
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

    @staticmethod
    def read_data():
        data, sender = Receiver.sock.recvfrom(1500)
        while data[-1:] == '\0':
            data = data[:-1]  # Strip trailing \0's
        print(str(sender) + '  ' + repr(data))
        data = data.decode()
        return data, sender
