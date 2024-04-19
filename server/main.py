from flask import Flask, request
import logging
import requests

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


from opentelemetry.sdk.resources import SERVICE_NAME, Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Service name is required for most backends
resource = Resource(attributes={
    SERVICE_NAME: "nesh-test-3"
})

traceProvider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces"))
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)

# reader = PeriodicExportingMetricReader(
#     OTLPMetricExporter(endpoint="localhost:4318/v1/metrics")
# )
# meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
# metrics.set_meter_provider(meterProvider)

tracer = trace.get_tracer("my.tracer.name")
from opentelemetry.instrumentation.requests import RequestsInstrumentor

RequestsInstrumentor(tracer_provider=traceProvider).instrument()

from opentelemetry.instrumentation.flask import FlaskInstrumentor

FlaskInstrumentor().instrument_app(app)

@app.route('/')
def hello_world():
    print(request.headers)
    # with tracer.start_as_current_span("hello_world") as span:
    return 'Hello, World!'

@app.route('/api1')
def api1():
    print(request.headers)
    # with tracer.start_as_current_span("api1") as span:
    logger.info('API1 was called')
    return 'API1'


@app.route('/api2')
def api2():
    print(request.headers)
    # with tracer.start_as_current_span("api2") as span:
    logger.info('API2 was called')
    return 'API2'

@app.route('/all')
def forall():
    print(request.headers)
    # with tracer.start_as_current_span("all") as span:
    resp1 = requests.get('http://localhost:5000/api1')
    resp2 = requests.get('http://localhost:5000/api2')
    return resp1.text +  resp2.text
        

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)