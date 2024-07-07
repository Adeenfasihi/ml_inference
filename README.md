
## Architecture

There are two deployments and two services. One each for the rabbitmq and the inference service.

### Rabbitmq

For rabbitmq, the configuration becomes easy with the use of rabbitmq management image. This gives us a dashboard to view running processes and provides us with a plethora of metrics.

What can be added to the config is the requests and limits of resources wherever a service is declared. The addition of federation and mirroring for fault-tolerance would be a good add-on as well.

### Inference-service

For the inference service, the image used is the one created by the dockerfile in the app directory. Docker installs all dependencies using the requirements.txt file and runs app.py exposing port 5000 for flask.

Here as well we can add requests and limits, along with the federation policy and mirroring.

In app.py we process the message taken in by the consumer. The consumer creates a channel in the rabbitmq service using plain credentials, declares a queue and starts a basic_consume that calls the process_message on callback.

The app.py also contains routes to check health for readiness and liveliness.

### Producer

This is a simple python file that creates a blocking connection to the rabbitmq channel using plain credentials, and uses basic publish to send the message that we want to process.

### Models

The models.py file includes an Abstract base class that gives us two methods which require implementation: "setup", and "infer". Setup is supposed to be where the model is set up and weights loaded etc. whereas infer takes in the text and gives it to the model to get an output. 

Here I have created a default model which is an entity recognition model. I used spacy and its english corpus to extract entities in text. We could use other models or differenc corpuses for this task and I just chose a basic one.


## Choices


### Flask

I chose flask because I have a little bit of prior experience in the framework from a hackathon I did recently. It is lightweight and easy to set up. It also helps that I am better versed in python than any other programming language. 

### Rabbitmq management

Given that I did know know rabbitmq at all before this, I used this because it gives us a nice dashboard and its online tutorials are easier to follow visually.

The other reason is that it is a publically available image and is looked after by the community, so we can just update the version and be good to go in the future.

### Repo structure

As we do at work, I like keeping the code files and the infrastructure files separate. This allows a team to work on relevant parts of the project without overlapping.

## Ideas for improvement

As this is the first time I created a rabbitmq app, I might not have all the ideas to improve, but I have listed down some basic ones in every section.

For the producer, we can have multiple of those that connect to the channel in rabbitmq and maintain state rather than running one time. 

For the app.py, we should also put the processed messages back in another queue for the consumers to take from and pass acknowledgements when done. This would mean we can have multiple nodes of rabbitmq in the cluster. One for input and processing, the other for output and consuming. For federated nodes, we shall have the same erlang cookie for all of the nodes and the same namespace.

Another thing we can add is autoscaling. The new node should have the same certificate and cookie to join the cluster.

## Security

Currently, for security I am using hardcoded username and password for rabbitmq. An obvious improvement to this is by adding a secrets deployment to a key management service and taking the credentials from there. 

Other than that, the cluster itself should be made a bit more secure and use certificate authentication.


## Steps:

Skip to 2. if not using minikube

```
eval $(minikube docker-env)
docker build --no-cache -t inference-service app/

kubectl apply -f namespace.yaml
kubectl apply -f rabbitmq_deployment.yaml
kubectl apply -f inference_deployment.yaml
```
Test deployments and svc
```
kubectl get pods -n ml-inference
kubectl get svc -n ml-inference
```
Port forward for all services
```
kubectl port-forward -n ml-inference svc/rabbitmq 15672:15672
kubectl port-forward -n ml-inference svc/rabbitmq 5672:5672
kubectl port-forward -n ml-inference svc/inference-service 8080:80
```
Produce message
```
python producer.py
```
Take note of the message-id and run to get the predicted output
```
curl http://localhost:8080/prediction/<message-id>
```

---
Step by step progression
---
## 1 - Service Setup

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

## 2 - Message Queue

1. kubectl apply -f namespace.yaml
2. kubectl apply -f deployment.yaml
3. kubectl apply -f service.yaml
    - uses rabbitmq3-management

*Test deployment:*
1. kubectl get pods -n ml-inference
2. kubectl get svc -n ml-inference
3. kubectl port-forward -n ml-inference svc/rabbitmq 15672:15672
    - for the management / dashboard

## 3 - Implement the service

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

Got stuck here because the inference-service was not running. Tried everything and chatgpt just gave command "imagePullPolicy: IfNotPresent" and the eval  command above that fixed it... Not sure how that works.

---

```
python producer.py
curl http://localhost:8080/prediction/<message-id>
```

## 4 - Model agnostic service

1. Create an abstract base class (ABC) in model.py
2. Extract the prediction algorithm from app.py
3. Put the NER algorithm into a concrete class of the ABC
4. Use the concrete class for prediction in app.py