# 1 - Service Setup

```
python3 -m venv ml
source ml/bin/activate
pip install --upgrade pip
pip install flask
python service.py
```

*Test endpoints*:
```
curl -X GET http://localhost:5000/v1/health/live
curl -X GET http://localhost:5000/v1/health/ready

```

