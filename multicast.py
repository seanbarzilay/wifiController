#!/usr/bin/env python

import argparse

group_4 = '225.0.0.250'
group_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'

parser = argparse.ArgumentParser()
parser.add_argument('-6', '--v6', default=False, action=argparse.BooleanOptionalAction, help="use ipv6")
parser.add_argument('-s', '--sender', default=False, action=argparse.BooleanOptionalAction, help='send data')
parser.add_argument('-k', '--keyboard', default=False, action=argparse.BooleanOptionalAction, help='emulate keyboard '
                                                                                                   'and mouse')
parser.add_argument('-t', '--type', default='desktop', help='reads input from a desktop machine')

args = parser.parse_args()


def main():
    group = group_6 if args.v6 else group_4

    if args.sender:
        start_sender(group)
    else:
        start_receiver(group)


def start_sender(group):
    if args.type == 'desktop':
        from senders.DesktopSender import DesktopSender
        DesktopSender(group)
    elif args.type == 'gpio':
        pass


def start_receiver(group):
    if args.keyboard:
        from receivers.KeyboardReceiver import KeyboardReceiver
        receiver = KeyboardReceiver(group)
    else:
        from receivers.GamepadReceiver import GamepadReceiver
        receiver = GamepadReceiver(group)
    receiver.start()


if __name__ == '__main__':
    main()
