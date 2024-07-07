from flask import Flask

app = Flask(__name__)

@app.route('/v1/health/live', methods=['GET'])
def liveness():
    return "OK", 200

@app.route('/v1/health/ready', methods=['GET'])
def readiness():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
