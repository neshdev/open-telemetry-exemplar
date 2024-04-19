import logging
import requests
from http.client import HTTPConnection
import uuid
import secrets

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HTTPConnection.debuglevel = 1

def traceparent():
    trace_32 = secrets.token_bytes(16).hex()
    trace_16 = secrets.token_bytes(8).hex()
    return f"00-{trace_32}-{trace_16}-01"

response = requests.get('http://localhost:5000/all', headers={'traceparent': traceparent() })
print("response is", response.text)
print(response)
