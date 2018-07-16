#!/usr/bin/python3
from flask import Flask, render_template, request
from quest import Quest
from configs.log_config import log_config
import logging.config
from observer import Observer
from events import Event, EventType
import time
import json
from devices import Device
import configs.device_config as device_cfg


app = Flask(__name__)
logging.config.dictConfig(log_config)
logger = logging.getLogger("saga")
devices = [getattr(device_cfg, device) for device in dir(device_cfg) if isinstance(getattr(device_cfg, device), Device)]

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
    return render_template("index.html", name=quest.name, layout=layout, timer=quest.get_time())


@app.route('/setup')
def setup():
    return render_template("setup.html", layout=layout, devices=devices, timer=0)


@app.route('/btn_click', methods=['GET', 'POST'])
def btn_click():
    btn_id = request.args.get('id', default="", type=str)
    if btn_id == "":
        return "fail"
    observer.push_event(Event(EventType.WEB_BUTTON_CLICKED, btn_id))
    return "ok"


@app.route('/poll', methods=['GET', 'POST'])
def poll():
    client_last_id = request.args.get('last_id', default=0, type=int)
    if client_last_id == 0:
        return json.dumps({"last_id": observer.last_id})

    while True:
        news = observer.poll_news(client_last_id)
        if news is not None:
            return json.dumps({'last_id': observer.last_id, 'events': news})
        else:
            time.sleep(1)


@app.template_filter('strftime')
def _jinja2_filter_time(time_):
    time_format = '%H:%M:%S'
    return time.strftime(time_format, time.gmtime(time_))


if __name__ == "__main__":
    logger.info("Program started")
    quest.start()
    app.run(port=8000, host='0.0.0.0', debug=True, use_reloader=False, threaded=True)
