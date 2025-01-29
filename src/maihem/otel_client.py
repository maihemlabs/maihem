from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


class Tracer:
    _instance = None

    def __init__(
        self, service_name="maihem-workflow", endpoint="http://127.0.0.1:4318/v1/traces"
    ):
        resource_attrs = {SERVICE_NAME: service_name}

        resource = Resource(attributes=resource_attrs)
        self.provider = TracerProvider(resource=resource)

        # Use OTLP HTTP exporter with BatchSpanProcessor
        otlp_exporter = OTLPSpanExporter(endpoint=endpoint)
        self.provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

        trace.set_tracer_provider(self.provider)
        self.tracer = trace.get_tracer(service_name)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Tracer()
        return cls._instance


def set_attribute(key: str, value: str):
    """Set an attribute on the current Maihem span."""
    current_span = trace.get_current_span()
    current_span.set_attribute(key, value)
