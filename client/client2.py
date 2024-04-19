import logging
import requests
from http.client import HTTPConnection
import uuid
import secrets

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HTTPConnection.debuglevel = 1

class TraceContext:
    def __init__(self):
        self.trace_32 = secrets.token_bytes(16).hex()
    
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _next_span(self):
        return secrets.token_bytes(8).hex()

    def next(self):
        trace_16 = secrets.token_bytes(8).hex()
        return f"00-{self.trace_32}-{trace_16}-01"


with TraceContext() as ctx:
    response1 = requests.get('http://localhost:5000/api1', headers={'traceparent': ctx.next() })
    response2 = requests.get('http://localhost:5000/api2', headers={'traceparent': ctx.next() })
    print("response is", response1.text)
    print(response1)
    print("response is", response2.text)
    print(response2)
