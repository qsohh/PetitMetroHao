# fixed block signalling


def simulate(dummies, stations, time, dt):
    for ele in dummies:
        ele.command(dt)
    for ele in stations:
        ele.control(time, dt)


def write_results():
    pass
