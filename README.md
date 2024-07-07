# 1 - Service Setup

```
cd service
docker build -t flask-app .
docker run -p 5000:5000 flask-app

```

*Test endpoints*:
```
curl -X GET http://localhost:5000/v1/health/live
curl -X GET http://localhost:5000/v1/health/ready

```

