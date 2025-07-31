#!/usr/bin/env python
import sys
sys.path.append('./DefClass')

from def_line import Track
from def_line import Line
from def_train import Train
from def_train import Position
from def_center import Center
from def_measure import Measure
from def_dummy import Dummy

time = 0.

def simulate(Line, Dummies):
    global time
    dt = 0.1
    run = True
#    while run:
    for dy in Dummies:
        tr = dy.train
        dy.state_set('RUN')
        dy.target_speed_cal()
        tr.target_speed = dy.target_speed

    for t in range(200):
        time += dt
        for dy in Dummies:
            tr = dy.train
            dy.state_set('RUN')
            dy.target_speed_cal()
            tr.target_speed = dy.target_speed
            if tr.target_speed>tr.speed:
                tr.speed += dt * tr.acceleration_positive
            tr.head.distance += tr.speed * dt * tr.direction
#            train.head.distance += train.speed * dt * train.direction


def main():
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    print('Current time: ', time)

    Track_1 = Track('Tr1', 800.)
    Position_1 = Position(Track_1, 80.)
    Train_1 = Train('90001', 80., Position_1, 0./3.6, [Track_1], 1)
    Line = [Track_1]
    Trains = [Train_1]

    Train_1.illustrate()

    Measure_1 = Measure(Train_1)

    Dummy_1 = Dummy(Measure_1)
    Dummies = [Dummy_1]

    simulate(Line, Dummies)

    print('Current time: ', time)
    Train_1.illustrate()



if __name__ == '__main__':

    main()
    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')