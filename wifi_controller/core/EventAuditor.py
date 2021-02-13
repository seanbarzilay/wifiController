import logging


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def audit_event(path: str, event: dict) -> None:
    with open(path, 'a') as f:
        f.write(str(event) + '\n')

