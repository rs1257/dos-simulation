import matplotlib.pyplot as p
import os

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
    p.plot(x, y1, 'bx')
    p.plot(x, y2, 'gx')
    p.plot(x, y3, 'rx')
    p.plot(x, y4, 'yx')
    p.legend(["Black Hole (Drop 1/1)", "Grey Hole (Drop 1/2)", "Grey Hole (Drop 1/3)", "Grey Hole (Drop 1/4)"])
    p.xlabel(xlabel)
    p.ylabel(ylabel + " (%)")

    location = r"c:\Users\Ryansmith\Desktop"
    if not os.path.isdir(location):
        print("Creating directory {0}".format(location))
        os.mkdir(location)
    p.savefig(location + "\\" + name + ".png")
    p.show()

if __name__ == '__main__':
    plot_packets_recieved()