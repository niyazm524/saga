from devices import *


# altar = []
# for i in range(1, 6):
#     altar.append(Altar("10.0.110.103", i))

altar1 = Altar(103, 5)
altar2 = Altar(103, 4)
altar3 = Altar(103, 3)
altar4 = Altar(103, 2)
altar5 = Altar(103, 1)

board = Board("/dev/ttyS0")

door1 = Door(114, 7, 1)
door2 = Door(105, 1, 2, from_uart=True)
door3 = Door(105, 2, 3, from_uart=True)
door4 = Door(115, 7, 4)
door5 = Door(108, 7, 5)
door6 = Door(116, 7, 6)
door7 = Door(117, 7, 7)


doors = [door1, door2, door3, door4, door5, door6, door7]
