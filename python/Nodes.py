class Mote:

    def __init__(self, MONITORED, ON, TX, RX, INT):
        self.NAME = MONITORED.split(" ", 1)[0]
        self.MONITORED = int(MONITORED.split(" ")[2])
        self.ON = int(ON.split(" ")[2])
        self.AVG_ON = (self.ON / float(self.MONITORED)) * 100
        self.TX = int(TX.split(" ")[2])
        self.AVG_TX = (self.TX / float(self.MONITORED)) * 100
        self.RX = int(RX.split(" ")[2])
        self.AVG_RX = (self.RX / float(self.MONITORED)) * 100
        self.INT = int(INT.split(" ")[2])
        self.AVG_INT = (self.INT / float(self.MONITORED)) * 100

    #round avgs for readibility
    def __repr__(self):
        return ("Name: {0} \nMonitored: {1} \nON: {2} AVG: {3} \nTX: {4} AVG: {5}  \nRX: {6} AVG: {7}  \nINT: {8} "
                "AVG: {9}\n".format(self.NAME, self.MONITORED, self.ON, round(self.AVG_ON, 2), self.TX,
                                  round(self.AVG_TX, 2), self.RX, round(self.AVG_RX, 2), self.INT,
                                  round(self.AVG_INT, 2)))