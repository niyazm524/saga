#!/usr/bin/python3
from urllib.request import urlopen

from flask import Flask, render_template, request
from quest import Quest
from configs.log_config import log_config
import logging.config
from observer import Observer
from events import Event, EventType
import time
import json
from player import Player, BGPlayer
from devices import Device
import configs.device_config as device_cfg
from configs.layout import gen_layout

app = Flask(__name__)
logging.config.dictConfig(log_config)
logger = logging.getLogger("Main")
# handler = TimedRotatingFileHandler(log_config["handlers"]["fileHandler"]["filename"],
#                                    when="d",
#                                    interval=1,
#                                    backupCount=5)
# logger.addHandler(handler)
devices = [getattr(device_cfg, device) for device in dir(device_cfg) if isinstance(getattr(device_cfg, device), Device)]

player = Player(volume=60)
bg_player = BGPlayer(volume=70)
quest = Quest("Скандинавская сага", player, bg_player, device_cfg)
observer = Observer(quest, device_cfg, player, bg_player)
layout = gen_layout(device_cfg)
device_cfg.altars.enable_notify(observer)


@app.route('/')
def index():
    return render_template("index.html", quest=quest, layout=layout, devices=device_cfg, timer=quest.get_time(),
                           aro=quest.aro, volume_bg=bg_player.volume,
                           ftime=quest.fulltime_minutes * 60, volume=player.volume,
                           now_playing=player.current_sound_file)


# @app.route('/setup')
# def setup():
#     return render_template("setup.html", layout=layout, devices=devices, timer=0, ftime=0)


def is_online(url, timeout=1000):
    try:
        print('Sending request to {}'.format(url))
        response = urlopen(url, timeout=timeout)
    except Exception:
        # Generally using a catch-all is a bad practice but
        # I think it's ok in this case
        response = False
        print('Request to {} failed'.format(url))
    if response:
        return True
    else:
        return False


@app.route('/power')
def power():
    power1 = True
    power2 = is_online("http://"+device_cfg.trunks.IP)
    power3 = is_online("http://"+device_cfg.horns.IP)
    powers = True
    print([powers, power1, power2, power3])
    return render_template("power.html", power=[powers, power1, power2, power3])


@app.route('/btn_click', methods=['GET', 'POST'])
def btn_click():
    btn_id = request.args.get('id', default="", type=str)
    btn_data = request.args.get('data', default="", type=str)
    if btn_id == "":
        return "fail"
    observer.button_clicked(btn_id, btn_data)
    return "ok"


@app.route('/btn-door', methods=['GET', 'POST'])
def btn_door():
    door = request.args.get('id', default="", type=str)
    action = request.args.get('data', default="", type=str)
    if door == "":
        return "fail"
    observer.door_clicked(door, action)
    return "ok"


@app.route('/btn-hint', methods=['GET', 'POST'])
def btn_hint():
    hint_id = request.args.get('id', default="", type=str)
    if hint_id == "":
        return "fail"
    observer.hint_clicked(hint_id)
    return "ok"


@app.route('/btn-actlink', methods=['GET', 'POST'])
def btn_actlink():
    id = request.args.get('id', default="", type=str)
    if id == "":
        return "fail"
    observer.actlink_clicked(id)
    return "ok"


@app.route('/poll', methods=['GET', 'POST'])
def poll():
    client_last_id = request.args.get('last_id', default=0, type=int)
    if client_last_id == 0:
        return json.dumps({"last_id": observer.last_id, "time": quest.get_time()})
    try:
        while True:
            news = observer.poll_news(client_last_id)
            if news is not None:
                return json.dumps({'last_id': observer.last_id, 'events': news, "time": quest.get_time(),
                                   'in_process': quest.in_process})
            else:
                time.sleep(1)
    except KeyboardInterrupt:
        return json.dumps({"last_id": 0})


@app.route('/sensors.php', methods=['GET', 'POST'])
def sensors():
    remote_ip = request.remote_addr
    _detected = request.args.get('detected', default="", type=str)
    detected = _detected == "true"
    pin = request.args.get('pin', default=0, type=int)
    for sensor in device_cfg.sensors:
        if remote_ip == sensor.IP:
            observer.push_event(Event(EventType.SENSOR_DATA_CHANGED, event_data={"detected": detected, "pin": pin},
                                      event_device=sensor))
            break

    return "ok"


@app.route('/altars', methods=['GET'])
def altars():
    data = request.args.get('data', default="", type=str)
    observer.push_event(Event(EventType.SENSOR_DATA_CHANGED, data, event_device=device_cfg.altars))
    return "ok"


@app.template_filter('strftime')
def _jinja2_filter_time(time_):
    time_format = '%H:%M:%S'
    return time.strftime(time_format, time.gmtime(time_))


if __name__ == "__main__":
    logger.warning("Program started")
    observer.push_event(Event(EventType.PROGRAM_STARTED))
    app.run(port=8000, host='0.0.0.0', debug=False, use_reloader=False, threaded=True)
