#!/usr/bin/env python

import argparse

from Receiver import Receiver
from Sender import Sender

group_4 = '225.0.0.250'
group_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'

parser = argparse.ArgumentParser()
parser.add_argument('-6', '--v6', default=False, action=argparse.BooleanOptionalAction, help="use ipv6")
parser.add_argument('-s', '--sender', default=False, action=argparse.BooleanOptionalAction, help='send data')

args = parser.parse_args()


def main():
    group = group_6 if args.v6 else group_4

    if args.sender:
        start_sender(group)
    else:
        start_receiver(group)


def start_sender(group):
    Sender(group)


def start_receiver(group):
    Receiver(group)


if __name__ == '__main__':
    main()
