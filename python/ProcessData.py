import matplotlib.pyplot as p
import os

from matplotlib import rcParams
rcParams.update({'figure.autolayout':True})

honest_resource_data = []
honest_packet_data = []
attack_resource_data = []
attack_packet_data = []

last = 0
convert_tick2sec = 0.000030517578125 # 1/32768
convert_sec2hour = 0.0002777777777778 # 1/3600
'''
extracts honest data and attackers data and plots them against each other
'''
def extract_data_and_plot(log, nodes, legend):
    fileh = log +  r"\logs\5hr.log"
    filea = log +  r"\logs\5hr-attack.log"
    data_dir = log + r"\graphs"

    global honest_resource_data, honest_packet_data
    honest_packet_data, honest_resource_data = read_file(fileh)
    global attack_resource_data, attack_packet_data
    attack_packet_data, attack_resource_data = read_file(filea)

    #honest_resource_data = calculate_radio(honest_resource_data)
    #attack_resource_data= calculate_radio(attack_resource_data)

    print_data(honest_resource_data)
    print('#################')
    print_data(attack_resource_data)

    #i screwed up some logs so this fixes them
    if "version" in log:
        honest_resource_data = remove_data(honest_resource_data, "ID:7")
        attack_resource_data = remove_data(attack_resource_data, "ID:7")

    plot_data_all(nodes, legend, data_dir)


def remove_data(data, field):
    newdata = []
    for value in data:
        print(value[17])
        if not field in value[17]:
            newdata.append(value)
    return newdata
'''
plots all relevant data on separate graphs
'''
def plot_data_all(nodes, legend, location):
    time = "Total Simulation Time"
    plot_data(nodes, legend, time, "Total Cpu Time", 1, location)
    plot_data(nodes, legend, time, "Total Low Power Mode Time", 2, location)
    plot_data(nodes, legend, time, "Total Transmit Time", 3, location)
    plot_data(nodes, legend, time, "Total Listen Time", 4, location)
    plot_data(nodes, legend, time, "Cpu Time", 5, location)
    plot_data(nodes, legend, time, "Low Power Mode Time", 6, location)
    plot_data(nodes, legend, time, "Transmit Time", 7, location)
    plot_data(nodes, legend, time, "Listen Time", 8, location)
    #plot_data(nodes, legend, time, "Total Radio Time", 9, location)
    #plot_data(nodes, legend, time, "Radio Time", 10, location)
    p.show()

'''
plot the two datasets against each other and save results to location
'''
def plot_data(nodes, legend, xlabel, ylabel, figure, location, all=1):
    p.figure(figure)

    name = "{0} against {1}".format(ylabel, xlabel)
    p.title(name)
    col1 = derive_vars(xlabel)
    col2 = derive_vars(ylabel)
    x, y = set_x_y(honest_resource_data, nodes, col1, col2)
    p.plot(x, y)
    x, y = set_x_y(attack_resource_data, nodes, col1, col2)
    p.plot(x, y)
    p.legend(legend)
    p.xlabel(xlabel + " (s)")
    p.ylabel(ylabel + " (s)")
    if not os.path.isdir(location):
        print("Creating directory {0}".format(location))
        os.mkdir(location)
    # p.savefig(location + "\\" + name + ".png")
    if all:
        p.draw()
    else:
        p.show()

'''
Retrieves correct columns from the graph labels to reduce human error
'''
def derive_vars(label):
    if label == "Total Simulation Time":
        return 1
    elif label == "Total Cpu Time":
        return 5
    elif label == "Total Low Power Mode Time":
        return 6
    elif label == "Total Transmit Time":
        return 7
    elif label == "Total Listen Time":
        return 8
    elif label == "Cpu Time":
        return 11
    elif label == "Low Power Mode Time":
        return 12
    elif label == "Transmit Time":
        return 13
    elif label == "Listen Time":
        return 14
    elif label == "Total Radio Time":
        return 16
    elif label == "Radio Time":
        return 17
    else:
        print("Invalid label: " + label)
        exit(1)

#placeholder function
def print_data(data):
    for line in data:
        print(line)
'''
opens data from a file, removes \n characters at the end of the lines, extracts lines containing #P 
and stores each line in a list after spliting it after every space
'''
def read_file(filename):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            if "#P" in line:
                entry = line.rstrip("\n")
                index = entry.find("#P")
                moteid = entry.split("\t")[1]
                entry = entry[index:].split(" ")
                entry.append(moteid) #add mote id to entry in case its needed later
                lines.append(entry)

    packets = []
    resources = []
    for entry in lines:
        entry[17:] = [' '.join((entry[17:]))]
        if entry[2] == 'P':
            resources.append(entry)
        elif entry[2] == 'SP':
            packets.append(entry)

    return (packets, resources)

'''
adds transmit and listen and all transmit and listen together and adds them to the data
'''
def calculate_radio(data):
    updated = []
    i = 0
    while i < len(data):
        entry = data[i]
        all_radio = int(data[i][6]) + int(data[i][7])
        radio = int(data[i][12]) + int(data[i][13])
        entry.append(all_radio)
        entry.append(radio)
        updated.append(entry)
        i+=1

    return updated

'''
returns an average value of each node for col1 and col2 (average over timestep for example)
'''
def set_x_y(data, nodes, col1, col2):
    i = 0
    global last
    x,y = [],[]
    while i < len(data):
        offset1 = 1
        offset2 = 1
        if col1 > 3:
            #this is the rtimer tick
            offset1 = 32768
        elif col1 == 1:
            #clock second
            offset1 = 128
        if col2 > 3:
            #this is the rtimer tick
            offset2 = 32768
        elif col2 == 1:
            #clock second
            offset2 = 128
        j = 0
        total1 = 0
        total2 = 0
        while j < nodes:
            #print(int(data[i + j][col2])/offset2)
            total1 += int(data[i + j][col1])
            total2 += int(data[i + j][col2])
            j+=1
        avg_col1 = (total1 / nodes) / offset1
        avg_col2 = (total2 / nodes) / offset2
        x.append(avg_col1)
        y.append(avg_col2)
        i+=nodes
        #if avg_col2 < last:
        #    print("HELPPPPPPPPPPPP")
        last = avg_col2
        #print("T:"  + str(avg_col2))
        #print("################")

    last = 0
    return x, y


def calculate_power(idletime, offtime, txtime, rxtime):
    #volatage for all modes
    v = 3
    #datasheet values for each mode in microA
    idle = 0.000426 * 1000000
    off = 0.00002 * 1000000
    tx = 0.0174 * 1000000
    rx = 0.0188 * 1000000

    #calculate total power usage for each state
    idlepower = v * idletime * idle
    offpower = v * offtime * off
    txpower = v * txtime * tx
    rxpower = v * rxtime * rx

    #sum to get total power usage - convert to seconds then to hours
    return ((idlepower + offpower + txpower + rxpower) * convert_tick2sec) * convert_sec2hour


def energest2power(energestval, current, voltage, runtime):
    top = energestval * current * voltage # mA * V = (mW * t) = mJ
    bottom = 32768.0 * (runtime / 128) #its mJ if you don't / runtime so mJ / t = mW, / 128 to convert to seconds
    return top / bottom

def power4all(normal, current, voltage, time):
    cpu = energest2power(normal[0], current[0], voltage, time)
    lpm = energest2power(normal[1], current[1], voltage, time)
    tx = energest2power(normal[2], current[2], voltage, time)
    rx = energest2power(normal[3], current[3], voltage, time)

    return cpu + lpm + tx + rx

def AvgModeCurrent(time, current):
    return (time * current)* convert_tick2sec

def AvgCurrent(cpuTime, cpuIdleTime, TxTime, RxTime):
    current = [0.000426, 0.00002, 0.0174, 0.0188]  # in mA
    cpu = AvgModeCurrent(cpuTime, current[0])
    cpuIdle = AvgModeCurrent(cpuIdleTime, current[1])
    Tx = AvgModeCurrent(TxTime, current[2])
    Rx = AvgModeCurrent(RxTime, current[3])
    return cpu + cpuIdle + Tx + Rx

def TotalTime(cpuTime, cpuIdleTime):
    return (cpuTime + cpuIdleTime) * convert_tick2sec / convert_tick2sec

def Charge(current, totalTime):
    return current * totalTime

def Power(current):
    return current * 3

def Energy(charge):
    return charge * 3

def plot_packets_recieved():
    ylabel = "Packets Dropped"
    xlabel = "Number of Nodes"

    x = [0, 1, 2, 3, 4, 5]

    # obtained by looking at logs
    y1 = [0, 20, 40, 60, 80, 100]
    y2 = [0, 10, 20, 30, 40, 50]
    y3 = [0, 6.67, 13.33, 20, 26.67, 33.33]
    y4 = [0, 5, 10, 15, 20, 25]
    name = "{0} against {1}".format("Packets Dropped", "Nodes sending to Malicious Node")
    p.title(name)
    p.plot(x, y1)
    p.plot(x, y2)
    p.plot(x, y3)
    p.plot(x, y4)
    p.legend(["Black Hole (Drop 1/1)", "Grey Hole (Drop 1/2)", "Grey Hole (Drop 1/3)", "Grey Hole (Drop 1/4)"])
    p.xlabel(xlabel)
    p.ylabel(ylabel + " (%)")

    location = "../selective-forwarding" + "/graphs"

    if not os.path.isdir(location):
        print("Creating directory {0}".format(location))
        os.mkdir(location)
    p.savefig(location + "\\" + name + ".png")
    p.show()

def plot_many(nodes, type, xlabel, ylabel, location, data):
    number = len(data)
    name = "{0} against {1} changing adjacent nodes".format(ylabel, xlabel)
    p.title(name)
    col1 = derive_vars(xlabel)
    col2 = derive_vars(ylabel)
    legend = []
    for i in range(number):
        x, y = set_x_y(data[i], nodes, col1, col2)
        p.plot(x, y)
        legend.append(str(i + 1) + " " + type)

    p.legend(legend)
    p.xlabel(xlabel + " (s)")
    p.ylabel(ylabel + " (s)")
    if not os.path.isdir(location):
        print("Creating directory {0}".format(location))
        os.mkdir(location)
    p.savefig(location + "\\" + name + ".png")
    p.show()


def counter(nodes, type, xlabel, ylabel, location):
    name = "{0} against {1}".format(ylabel, xlabel)
    p.title(name)
    col1 = derive_vars(xlabel)
    col2 = derive_vars(ylabel)
    legend = ["Honest", "Attack", "Countermeasure"]
    _, tmp = read_file(log + "/logs/" + "5hr.log")
    x, y = set_x_y(tmp, nodes, col1, col2)
    p.plot(x, y)
    _, tmp = read_file(log + "/logs/" + "5hr-attack.log")
    x, y = set_x_y(tmp, nodes, col1, col2)
    p.plot(x, y)
    _, tmp = read_file(log + "/logs/" + "counter.log")
    x, y = set_x_y(tmp, nodes, col1, col2)
    p.plot(x, y)
    p.legend(legend)
    p.xlabel(xlabel + " (s)")
    p.ylabel(ylabel + " (s)")
    if not os.path.isdir(location):
        print("Creating directory {0}".format(location))
        os.mkdir(location)
    #p.savefig(location + "\\" + name + ".png")
    p.show()

def plot_many_legend(nodes, xlabel, ylabel, location, data, legend, mode="any"):
    number = len(data)
    name = "{0} against {1}".format(ylabel, xlabel)

    p.title(name)

    col1 = derive_vars(xlabel)
    col2 = derive_vars(ylabel)

    options = ["H, R, S", "F", "V", "S", "R", "HF", "F, HF"]
    for i in range(number):
        x, y = set_x_y(data[i], nodes, col1, col2)
        p.plot(x, y)
        p.xlim(0, 20000)
        if not (options[i] == "R" or options[i] == "S"):
            if mode == 'tx':
                if options[i] == "F":
                    p.annotate(options[i], (x[-1] + (x[-1] * 0.01), y[-1] + 5), va='center')
                elif options[i] == "HF":
                    p.annotate(options[i], (x[-1] + (x[-1] * 0.01), y[-1] - 5), va='center')
                else:
                    p.annotate(options[i], (x[-1] + (x[-1] * 0.01), y[-1]), va='center')
            elif mode == 'lpm':
                if not options[i] == "HF":
                    if options[i] == "H, R, S":
                        p.annotate(options[i], (x[-1] + (x[-1] * 0.01), y[-1] + 200), va='center')
                    elif options[i] == "F":
                        p.annotate(options[6], (x[-1] + (x[-1] * 0.01), y[-1]), va='center')
                    else:
                        p.annotate(options[i], (x[-1] + (x[-1] * 0.01), y[-1]), va='center')
            else:
                p.annotate(options[i], (x[-1] + (x[-1] * 0.01), y[-1]), va='center')


    p.legend(legend)
    p.xlabel(xlabel + " (s)")
    p.ylabel(ylabel + " (s)")
    if not os.path.isdir(location):
        print("Creating directory {0}".format(location))
        os.mkdir(location)
    p.savefig(location + "\\" + name + ".png")

    p.show()

if __name__ == '__main__':
    flood = "../packet-flood"
    version = "../increased-version"
    selectiveforwarding = "../selective-forwarding"
    rank = "../decreased-rank"
    hello = "../hello-flood"
    log = flood
    nodes = 5
    legenda = "Honest"
    legendb = "Packet Flood"
    normal = [158645, 9365005, 26202, 67595] #time = 37305
    attack1 = [585711, 8937939, 259995, 217313] #time = 37305
    attack2 = [57710, 1171540, 22314, 20730] #time = 4905

    #print(calculate_power(attack1[0], attack1[1], attack1[2], attack1[3]))
    #counter(5, "Counter", "Total Simulation Time", "Total Cpu Time", log + "/graphs/counter")
    #counter(5, "Counter", "Total Simulation Time", "Total Transmit Time", log + "/graphs/counter")
    #counter(5, "Counter", "Total Simulation Time", "Total Listen Time", log + "/graphs/counter")
    #counter(5, "Counter", "Total Simulation Time", "Total Low Power Mode Time", log + "/graphs/counter")
    #current = [0.426, 0.02, 17.4, 18.8] #in mA
    '''
    with open(log + "/logs/" + "2hop.log" , "r") as f:
        lines = []
        for line in f:
            print(line)
    '''
    '''data = []
    numlogs = 6
    for i in range(numlogs):
        _, tmp = read_file(log + "/logs/" + str(i + 1) + "adj.log")
        data.append(tmp)

    label = "Adjacent"
    plot_many(10, label, "Total Simulation Time", "Total Cpu Time", log + "/graphs", data)
    plot_many(10, label, "Total Simulation Time", "Total Transmit Time", log + "/graphs", data)
    plot_many(10, label, "Total Simulation Time", "Total Listen Time", log + "/graphs", data)
    plot_many(10, label, "Total Simulation Time", "Total Low Power Mode Time", log + "/graphs", data)
    '''
    #print("Power - " + str(power4all(attack1, current, 3, 37305)) + " mW") #avg power comsumption
    #print("Power per hour - " + str(power4all(attack1, current, 3, 37305) * convert_sec2hour) + " mWh")  # mWh
    #print("Total Energy - " + str(power4all(attack1, current, 3, 128)) + " mJ")  # avg power comsumption
    #extract_data_and_plot(log, nodes, [legenda, legendb])

    '''loggy = log + r"\logs\counter.log"

    _, dta = read_file(loggy)
    index = len(dta)
    print(dta[index - 5]) # as starts at 0 subtract an extra 1
    tcpu = 0
    tlpm = 0
    ttx = 0
    trx = 0
    for i in range(5):
        tcpu += int(dta[index - 5 + i][5])
        tlpm += int(dta[index - 5 + i][6])
        ttx += int(dta[index - 5 + i][7])
        trx += int(dta[index - 5 + i][8])

    normal[0] = tcpu / 5
    normal[1] = tlpm / 5
    normal[2] = ttx / 5
    normal[3] = trx / 5

    current = AvgCurrent(normal[0], normal[1], normal[2], normal[3])
    totalTime = TotalTime(normal[0], normal[1])
    charge = Charge(current, totalTime)
    power = Power(current)
    energy = Energy(charge)

    print("Current: {0}mA, Total Time: {1}s, Charge: {2}mC, Power: {3}mW,  Energy: {4}mJ".format(round(current, 3),
                            round(totalTime, 3), round(charge, 3), round(power, 3), round(energy, 3)))

    '''
    #plot_packets_recieved()
    data = []
    atks = [flood, version, selectiveforwarding, rank, hello]
    _, tmp = read_file(flood + "/logs/" + "5hr.log")
    data.append(tmp)
    for i in atks:
        _, tmp = read_file(i + "/logs/" + "5hr-attack.log")
        if "version" in i:
            tmp = remove_data(tmp, "ID:7")
        data.append(tmp)

    print_data(data)

    legend = ["Honest Network (H)", "Packet Flooding (F)", "Versioning Attack (V)", "Selective Forwarding (S)", "Rank Attack (R)", "Hello Flood (HF)"]
    plot_many_legend(nodes, "Total Simulation Time", "Total Cpu Time", log + "/graphs", data, legend)
    plot_many_legend(nodes, "Total Simulation Time", "Total Transmit Time", log + "/graphs", data, legend, mode='tx')
    plot_many_legend(nodes, "Total Simulation Time", "Total Listen Time", log + "/graphs", data, legend)
    plot_many_legend(nodes, "Total Simulation Time", "Total Low Power Mode Time", log + "/graphs", data, legend, mode='lpm')
