#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def fastapi_instrumentor(app):
    FastAPIInstrumentor().instrument_app(app)