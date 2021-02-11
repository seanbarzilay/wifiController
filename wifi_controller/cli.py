"""Console script for wifi_controller."""
import argparse
import sys


def main():
    """Console script for wifi_controller."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-6', '--v6', default=False, action=argparse.BooleanOptionalAction, help="use ipv6")
    parser.add_argument('-s', '--sender', default=False, action=argparse.BooleanOptionalAction, help='send data')
    parser.add_argument('-k', '--keyboard', default=False, action=argparse.BooleanOptionalAction,
                        help='emulate keyboard '
                             'and mouse')
    parser.add_argument('-t', '--type', default='desktop', help='reads input from a desktop machine')
    parser.add_argument('-c', '--config', type=str, help='config file for gpio sender')
    parser.add_argument('-a', '--audit', type=argparse.BooleanOptionalAction, help='audit events')
    args = parser.parse_args()

    group_4 = '225.0.0.250'
    group_6 = 'ff15:7079:7468:6f6e:6465:6d6f:6d63:6173'

    group = group_6 if args.v6 else group_4

    if args.sender:
        start_sender(group, args.type, args.config, args.audit)
    else:
        start_receiver(group, args.keyboard, args.audit)
    return 0


def start_sender(group, sender_type, config, audit):
    if sender_type == 'desktop':
        from wifi_controller.senders.DesktopSender import DesktopSender
        DesktopSender(group)
    elif sender_type == 'gpio':
        from wifi_controller.senders.GpioSender import GpioSender
        with open(config, 'r') as conf:
            import yaml
            config = yaml.safe_load(conf)
        GpioSender(group, config, audit)


def start_receiver(group, keyboard, audit):
    if keyboard:
        from wifi_controller.receivers.KeyboardReceiver import KeyboardReceiver
        receiver = KeyboardReceiver(group)
    else:
        from wifi_controller.receivers.GamepadReceiver import GamepadReceiver
        receiver = GamepadReceiver(group, audit)
    receiver.start()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
