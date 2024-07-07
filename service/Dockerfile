FROM python:3.9-slim

WORKDIR /app

COPY . .

# No requirements.txt for now
RUN pip install --no-cache-dir Flask

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

CMD ["python", "app.py"]
