from devices import *


# altar = []
# for i in range(1, 6):
#     altar.append(Altar("10.0.110.103", i))

altar1 = Altar("10.0.110.103", 1)
altar2 = Altar("10.0.110.103", 2)
altar3 = Altar("10.0.110.103", 3)
altar4 = Altar("10.0.110.103", 4)
altar5 = Altar("10.0.110.103", 5)

board = Board("/dev/ttyS0")

door1 = Door("10.0.110.114", 7, 1)
