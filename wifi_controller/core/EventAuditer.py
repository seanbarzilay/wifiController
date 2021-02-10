import logging
import requests

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def audit_event(path: str, event: dict) -> None:
    res = requests.post(f"http://seans-pc:9200/{path}/_doc", json=event)
    print(repr(res))
    if res.status_code > 201:
        logging.debug(repr(res))
