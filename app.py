import os
import sys
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect, request

app = Flask(__name__)
app.secret_key = "randomsecretkey"
app.config["MONGO_DBNAME"] = 'memory'
app.config["MONGO_URI"] = 'mongodb://admin:Admin@ds155045.mlab.com:55045/memory'

mongo = PyMongo(app)

@app.route('/')
def main():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)