import logging
import requests

logger = logging.getLogger("KodeArrow.Network")


def check_internet_connection():
    try:
        requests.get("http://www.google.com", timeout=5)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False
