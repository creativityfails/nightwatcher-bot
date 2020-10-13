import time


def userlimits(file):
    with open(file) as f:
        users = [[int(x) for x in line.strip().split(",")] for line in f]
    return users


def checklimit(limits, user):
    for l in limits:
        if user == l[0]:
            if (time.time() - l[2]) > 86400:
                l[2] = int(time.time()/86400) * 86400
                l[1] = l[3]
            if l[1] == 0:
                return False
            if l[1] > 0:
                l[1] -= 1
                return True
    return True


def adduser(idn, limit, limits):
    limits.append([idn, limit, int(time.time()/86400) * 86400, limit])


def filewrite(file, limits):
    f = open(file, "w")
    for l in limits:
        f.write(f"{l[0]},{l[1]},{l[2]},{l[3]}\n")

