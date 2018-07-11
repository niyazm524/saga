#!/usr/bin/python3
from flask import Flask, render_template
from quest import Quest
from log_config import log_config
import logging, logging.config

app = Flask(__name__)
quest = Quest("Saga")
logging.config.dictConfig(log_config)
logger = logging.getLogger("saga")

@app.route('/')
def index():
    return render_template("index.html", name=quest.name)


if __name__ == "__main__":
    logger.info("Program started")
    quest.start()
    app.run(port=8000, host='0.0.0.0', debug=True, use_reloader=False, threaded=True)
