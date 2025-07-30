# OpenTelemetryPython公共库

## 构建pypi源
```shell
pip install setuptools wheel twine
python setup.py sdist bdist_wheel
twine upload dist/*
```