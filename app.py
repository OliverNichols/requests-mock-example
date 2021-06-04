from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def index():
    example_text = requests.get('http://backend:5000/get/text').text # doesn't exist
    return f'{example_text}\n'

if __name__ == '__main__':
    app.run(host='0.0.0.0')