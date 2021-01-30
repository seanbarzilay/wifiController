import socket
import struct


class Receiver:
    sock = None
    port = 8123
    address = None

    def __init__(self, group) -> None:
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
        Receiver.sock = s

    @staticmethod
    def read_data():
        data, sender = Receiver.sock.recvfrom(1500)
        while data[-1:] == '\0':
            data = data[:-1]  # Strip trailing \0's
        print(str(sender) + '  ' + repr(data))
        data = data.decode()
        return data, sender
