#!/usr/bin/env python3
# -*- coding:utf-8 -*-


from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor


def kafka_instrumentor():
    AIOKafkaInstrumentor().instrument()