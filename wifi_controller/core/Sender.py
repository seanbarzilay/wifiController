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
