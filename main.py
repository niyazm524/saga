#!/usr/bin/python3
from flask import Flask, render_template, request
from quest import Quest
from log_config import log_config
import logging, logging.config
from observer import Observer
from events import Event, EventType
import json


app = Flask(__name__)
logging.config.dictConfig(log_config)
logger = logging.getLogger("saga")
observer = Observer(logger)
quest = Quest("Скандинавская сага", observer)
try:
    layout_file = open("layout.json", 'r')
    layout_content = layout_file.read()
    if layout_content == "":
        layout_content = "[]"
    layout = json.loads(layout_content)
except ValueError:
    logger.error("Can't deserialize layout!")
    logger.error("Quitting..")
    raise SystemExit()


@app.route('/')
def index():
    return render_template("index.html", name=quest.name, layout=layout)


@app.route('/setup')
def setup():
    return render_template("setup.html", layout=layout)


@app.route('/btn_click', methods=['GET', 'POST'])
def btn_click():
    btn_id = request.args.get('id', default="", type=str)
    if btn_id == "":
        return "fail"
    observer.push_event(Event(EventType.WEB_BUTTON_CLICKED, btn_id))
    return "ok"


if __name__ == "__main__":
    logger.info("Program started")
    quest.start()
    app.run(port=8000, host='0.0.0.0', debug=True, use_reloader=False, threaded=True)
