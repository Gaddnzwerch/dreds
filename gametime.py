class Gametime():
    tickcount = 0 

    def nextTick():
        Gametime.tickcount += 1

    nextTick = staticmethod(nextTick)
