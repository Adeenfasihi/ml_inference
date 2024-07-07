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

1. kubectl create namespace ml_inference
2. kubectl apply -f namespace.yaml
3. kubectl apply -f deployment.yaml
4. kubectl apply -f service.yaml

1. kubectl get pods -n ml-inference
2. kubectl get svc -n ml-inference
3. kubectl port-forward -n ml-inference svc/rabbitmq 15672:15672