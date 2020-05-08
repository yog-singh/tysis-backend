import os
from flask import Flask, flash, request, redirect, url_for

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def basic():
    if request.method == 'POST':
        return 'Hello World'