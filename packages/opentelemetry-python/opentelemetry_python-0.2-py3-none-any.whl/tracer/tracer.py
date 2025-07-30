#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.propagate import set_global_textmap
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator


def init_tracer(export_endpoint: str, project_name: str, command: str, attributes: dict = None):
    exporter = OTLPSpanExporter(endpoint=export_endpoint, insecure=True)

    default_attributes = {
        "service.name": command,
        "project.name": project_name,
        "project.command": command,
    }

    if attributes:
        default_attributes.update(attributes)

    resource = Resource(default_attributes)

    provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(provider)

    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    set_global_textmap(TraceContextTextMapPropagator())

    def shutdown():
        provider.force_flush()

    return shutdown
