# OpenTelemetry Exemplar

The opentelemetry is setup on python flask server with automatic instrumentation for flask and requests library.

The client can propagate the telemetry using the header `TraceParent`. A simple propogation is used in the client to add the `TraceParent` header. The simple approach will keep the client side library light weigth without dependencies.

## Instructions

1. Start the jager collector `./collector\jaeger.sh`
2. Start the python server `python ./server\main.py`
3. Run the client `./client\client2.py`
4. View the trace on jaeger UI. (http://localhost:16686)

## Help

TraceParent - https://www.w3.org/TR/trace-context/#traceparent-header-field-values
OpenTelemetry - https://opentelemetry.io/docs/languages/python/getting-started/