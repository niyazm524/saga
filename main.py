#!/usr/bin/python3
from flask import Flask, render_template
from quest import Quest

app = Flask(__name__)
quest = Quest()

@app.route('/')
def hello_world():
    return render_template("index.html")


if __name__ == "__main__":
    quest.start()
    app.run(port=8000, host='0.0.0.0', debug=True, use_reloader=False)