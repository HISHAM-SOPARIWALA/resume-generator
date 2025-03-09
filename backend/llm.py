from flask import Flask, request, jsonify
import groq
from dotenv import load_dotenv
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, welcome to the Flask API!"

@app.route('/api/echo', methods=['POST'])
def echo():
    data = request.get_json()
    return jsonify(data)

@app.route('/api/greeting/<name>')
def greeting(name):
    return jsonify({"message": f"Hello, {name}!"})

if __name__ == '__main__':
    app.run(debug=True)