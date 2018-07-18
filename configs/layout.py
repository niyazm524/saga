
def gen_layout(device_cfg):
    rooms = [
        {"name": "Подсказки",
         "buttons": [],
         "hints": []},

        {"name": "Комната алтарей",
         "buttons": [device_cfg.door1]},

        {"name": "Маски",
         "buttons": [device_cfg.door2, device_cfg.masks_trunk]},

        {"name": "Сундуки",
         "buttons": [device_cfg.door3]},

        {"name": "RFID",
         "buttons": [device_cfg.door4]},

        {"name": "Эквалайзер",
         "buttons": [device_cfg.door5, device_cfg.tumba]},

        {"name": "Древо",
         "buttons": [device_cfg.door6, device_cfg.tree]},

        {"name": "Барабан",
         "buttons": [device_cfg.door7, device_cfg.barrel]},


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
                        rooms.append({"name": line[0], "hints": [dict(id=line[1], desc=line[3])]})
                else:
                    rooms[0]["hints"].append(dict(id=line[1], desc=line[3]))
            else:
                rooms[room]["hints"] = [dict(id=line[1], desc=line[3])]

    return rooms

