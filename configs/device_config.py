from devices import *


# altar = []
# for i in range(1, 6):
#     altar.append(Altar("10.0.110.103", i))

altars = Altars(103)

board = Board("/dev/ttyS0")

door1 = EspDoor(114, 7, 1)
door2 = UartDoor(105, 1, 2)
door3 = UartDoor(105, 2, 3)
door4 = EspDoor(115, 7, 4)
door5 = AlexDoor(108, index=5, btn_id="door5", cls_type="Эквалайзер")

door6 = EspDoor(116, 7, 6)
door7 = EspDoor(117, 7, 7)

# masks_trunk = UartDoor(104, 1, btn_id="masks_trunk", cls_type="Сундук с масками", index="")
tumba = PhpDoor(107, cls_type="Тумба", btn_id="tumba")
tree = AlexDoor(109, btn_id="tree", cls_type="Древо", )
barrel = AlexDoor(112, cls_type="Барабан", btn_id="barrel")


trunks = Device(DeviceType.TRUNKS, 105)

ems = [door1, door2, door3, door4, door5, door6, door7, tumba, tree, barrel]

sensors = [trunks, tree, door5, barrel]
