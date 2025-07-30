from setuptools import setup, find_packages

setup(
    name='opentelemetry-python',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'opentelemetry-api==1.33.1',
        'opentelemetry-sdk==1.33.1',
        'opentelemetry-exporter-otlp==1.33.1',
        'opentelemetry-instrumentation-fastapi==0.54b1',
        'opentelemetry-instrumentation-grpc==0.54b1',
        'opentelemetry-instrumentation-aiokafka==0.54b1',
    ],
)