#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from opentelemetry.instrumentation.grpc import GrpcInstrumentorClient, GrpcInstrumentorServer
from opentelemetry.instrumentation.grpc import GrpcAioInstrumentorClient, GrpcAioInstrumentorServer


def grpc_instrumentor_client():
    GrpcInstrumentorClient().instrument()


def grpc_instrumentor_server():
    GrpcInstrumentorServer().instrument()


def grpc_instrumentor_aio_client():
    GrpcAioInstrumentorClient().instrument()

def grpc_instrumentor_aio_server():
    GrpcAioInstrumentorServer().instrument()