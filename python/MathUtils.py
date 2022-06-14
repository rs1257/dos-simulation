#result is unrounded for accuracy
def get_avg(MOTES, type):
    total = 0.0
    for m in MOTES:
        if type == "ON":
            total += m.AVG_ON
        elif type == "TX":
            total += m.AVG_TX
        elif type == "RX":
            total += m.AVG_RX
        elif type == "INT":
            total += m.AVG_INT

    return (total / len(MOTES))

#result is unrounded for accuracy
def get_avg_all(MOTES):
    result = []
    result.append(get_avg(MOTES, "ON"))
    result.append(get_avg(MOTES, "TX"))
    result.append(get_avg(MOTES, "RX"))
    result.append(get_avg(MOTES, "INT"))
    return result

def diff_avg(m1, m2):
    r1 = get_avg_all(m1)
    r2 = get_avg_all(m2)
    i = 0
    result = []
    while i < 4:
        result.append(r2[i] - r1[i])
        i+=1

    return result