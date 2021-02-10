import logging
import requests
import _thread

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)


def audit_event(path: str, event: dict) -> None:
    def audit():
        res = requests.post(f"http://seans-pc:9200/{path}/_doc", json=event)
        print(repr(res))
        if res.status_code > 201:
            logging.debug(repr(res))
    _thread.start_new_thread(audit, ())
