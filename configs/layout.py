
def gen_layout(device_cfg):
    rooms = [
        {"name": "Комната алтарей",
         "buttons": [device_cfg.door1]},

        {"name": "Маски",
         "buttons": [device_cfg.door2]},

        {"name": "Сундуки",
         "buttons": [device_cfg.door3]},

        {"name": "RFID",
         "buttons": [device_cfg.door4, device_cfg.horns],
         "actlinks": [{"name": "-2 аро", "id": "minus2aro"}]},

        {"name": "Эквалайзер",
         "buttons": [device_cfg.door5, device_cfg.tumba]},

        {"name": "Древо",
         "buttons": [device_cfg.door6, device_cfg.tree, device_cfg.ropes_locker]},

        {"name": "Барабан",
         "buttons": [device_cfg.door7, device_cfg.barrel]},

        {"name": "Подсказки",
         "buttons": [],
         "hints": []},
    ]

    with open("configs/hints.csv", "r") as hints:
        lines = hints.read().splitlines()
        for line in lines:
            line = line.split(';')
            try:
                room = int(line[0])
            except ValueError:
                if len(line[0]) > 0:
                    for room in rooms:
                        if room["name"] == line[0]:
                            room["hints"].append(dict(id=line[1], desc=line[3]))
                            break
                    else:
                        rooms
                        rooms.append({"name": line[0], "hints": [dict(id=line[1], desc=line[3])]})
                else:
                    rooms[-1]["hints"].append(dict(id=line[1], desc=line[3]))
            else:
                if "hints" in rooms[room]:
                    rooms[room]["hints"].append(dict(id=line[1], desc=line[3]))
                else:
                    rooms[room]["hints"] = [dict(id=line[1], desc=line[3])]

    return rooms

# import configs.device_config
# import pprint
# pprint.pprint(gen_layout(configs.device_config))