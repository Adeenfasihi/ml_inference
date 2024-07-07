# 1 - Service Setup

```
cd service
docker build -t flask-app .
docker run -p 5000:5000 flask-app
```

*Test endpoints:*
```
curl -X GET http://localhost:5000/v1/health/live
curl -X GET http://localhost:5000/v1/health/ready
```

# 2 - Message Queue

1. kubectl apply -f namespace.yaml
2. kubectl apply -f deployment.yaml
3. kubectl apply -f service.yaml
    - uses rabbitmq3-management

*Test deployment:*
1. kubectl get pods -n ml-inference
2. kubectl get svc -n ml-inference
3. kubectl port-forward -n ml-inference svc/rabbitmq 15672:15672
    - for the management / dashboard

# 3 - Implement the service

1. cd app
```
eval $(minikube docker-env)
```
2. docker build -t inference-service .
3. cd ..
4. cd infrastructure
5. kubectl apply -f inference_service.yaml
6. kubectl port-forward -n ml-inference svc/rabbitmq 5672:5672
7. kubectl port-forward -n ml-inference svc/inference-service 8080:80

---

```
python producer.py
curl http://localhost:8080/prediction/<message-id>
```



Got stuck here because the inference-service was not running. Tried everything and chatgpt just gave command "imagePullPolicy: IfNotPresent" and the eval  command above that fixed it... Not sure how that works.