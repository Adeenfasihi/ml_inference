FROM python:3.9-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Make port 5000 available to the world outside this container
EXPOSE 5000

CMD ["python", "app.py"]
