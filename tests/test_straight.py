#!/usr/bin/env python
import sys
sys.path.append('./DefClass')

from def_line import Track
from def_line import Line
from def_line import Node
from def_train import Train
from def_train import Position
from def_center import Center
from def_measure import Measure
from def_dummy import Dummy
from def_environment import Environment
import matplotlib.pyplot as plt

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
    # sn0 = Node('sn0')
    # sn1 = Node('sn1')
    # tr0_1 = Track('tr0_1', 700., sn0, sn1)
    # tr1_0 = Track('tr1_0', 800., sn0, sn1)
    # for ele in sn0.list_tracks_node:
    #     print(ele.name)
    # tr0_1.print_track()
    # tr1_0.print_track()
    # sn0.signal = True
    # tr0_1.update_track()
    # tr0_1.print_track()

    # test_self_circle_line()
    # test_switch_direction()

    # print('Current time:', time)

    # set of the nodes
    sn0 = Node('sn0')
    sn1 = Node('sn1')
    sn2 = Node('sn2')
    sn3 = Node('sn3')
    sn4 = Node('sn4')
    sn5 = Node('sn5')
    sn6 = Node('sn6')
    sn7 = Node('sn7')
    sn8 = Node('sn8')
    sn9 = Node('sn9')
    sn10 = Node('sn10')
    sn11 = Node('sn11')

    # set of the tracks
    tr0_1_6 = Track('tr0_1_6', 70., sn0, sn1)
    tr1_2 = Track('tr1_2', 200., sn1, sn2)
    tr2_3 = Track('tr2_3', 200., sn2, sn3)
    tr3_4 = Track('tr3_4', 200., sn3, sn4)
    tr5_4_11 = Track('tr5_4_11', 70., sn5, sn11)
    tr6_7 = Track('tr6_7', 20., sn6, sn7)
    tr7_8 = Track('tr7_8', 190., sn7, sn8)
    tr8_9 = Track('tr8_9', 200., sn8, sn9)
    tr9_10 = Track('tr9_10', 190., sn9, sn10)
    tr10_11 = Track('tr1_0', 20., sn10, sn11)

    # state of sn1
    sn1.signal = True
    sn2.signal = True
    sn3.signal = True
    sn7.signal = True
    sn8.signal = True
    sn9.signal = True
    sn10.signal = True
    sn11.signal = True

    # set of line
    line1 = Line('Line1', tr0_1_6)
    line1.print_line()
    line2 = Line('Line2', tr5_4_11)
    line2.print_line()


################################################################################
def test_self_circle_line():
    print('Test of self-circle line:')
    # set of the nodes
    sn0 = Node('sn0')
    sn1 = Node('sn1')

    # set of the tracks
    tr0_1 = Track('tr0_1', 700., sn0, sn1)
    tr1_2 = Track('tr1_2', 750., sn1, sn0)

    # state of nodes
    sn1.signal = True
    sn0.signal = True
    tr0_1.track_next = tr1_2
    tr1_2.track_next = tr0_1
    tr1_2.track_pre = tr0_1
    tr0_1.track_pre = tr1_2

    # set of line
    linet = Line('circle', tr0_1)
    linet.print_line()
    print(linet.iscircle)

def test_switch_direction():
    print('Test of case switch direction:')
    # set of the nodes
    sn0 = Node('sn0')
    sn1 = Node('sn1')
    sn2 = Node('sn2')

    # set of the tracks
    tr0_1 = Track('tr0_1', 700., sn0, sn1)
    tr1_2 = Track('tr1_2', 750., sn1, sn2)
    tr2_0 = Track('tr2_0', 700., sn2, sn0)

    # state of nodes
    sn1.signal = True
    sn0.signal = True
    sn2.signal = True
    tr0_1.track_next = tr1_2
    tr1_2.track_next = tr2_0
    tr2_0.track_next = tr0_1
    tr1_2.track_pre = tr0_1
    tr0_1.track_pre = tr2_0
    tr2_0.track_pre = tr1_2

    # set of line
    linet = Line('circle3', tr0_1)
    print('Before the switch of direction:')
    linet.print_line()
    tr0_1.switch_direction()
    linet.update_line()
    print('After the switch of direction:')
    linet.print_line()

def test_self_circle_headback_line():
    print('Test of self-circle-headback line:')
    # set of the nodes
    sn0 = Node('sn0')
    sn1 = Node('sn1')
    sn2 = Node('sn2')
    sn3 = Node('sn3')

    # set of the tracks

if __name__ == '__main__':
    # main()
    # set of the nodes

    print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

sn0 = Node('sn0')
sn1 = Node('sn1')
sn2 = Node('sn2')
sn3 = Node('sn3')
sn4 = Node('sn4')
sn5 = Node('sn5')
sn6 = Node('sn6')
sn7 = Node('sn7')
sn8 = Node('sn8')
sn9 = Node('sn9')
sn10 = Node('sn10')
sn11 = Node('sn11')
sn12 = Node('sn12')
sn13 = Node('sn13')
sn14 = Node('sn14')
sn15 = Node('sn15')

# set of the tracks
tr0_1_8 = Track('tr0_1_8', 70., sn0, sn1, 5.)
tr1_2 = Track('tr1_2', 200., sn1, sn2, 50.)
tr2_3 = Track('tr2_3', 100., sn2, sn3, 50.)
tr3_4 = Track('tr3_4', 50., sn3, sn4, 25.)
tr4_5 = Track('tr4_5', 100., sn4, sn5, 50.)
tr5_6 = Track('tr5_6', 200., sn5, sn6, 50.)
tr7_6_15 = Track('tr7_6_15', 70., sn7, sn15, 5.)
tr8_9 = Track('tr8_9', 20., sn8, sn9, 20.)
tr9_10 = Track('tr9_10', 190., sn9, sn10, 50.)
tr10_11 = Track('tr10_11', 100., sn10, sn11, 50.)
tr11_12 = Track('tr11_12', 50, sn11, sn12, 25.)
tr12_13 = Track('tr12_13', 100., sn12, sn13, 50.)
tr13_14 = Track('tr13_14', 190., sn13, sn14, 50.)
tr14_15 = Track('tr14_15', 20., sn14, sn15, 20.)

# state of sn1
sn1.signal = True
sn2.signal = True
sn3.signal = True
sn4.signal = True
sn5.signal = True
sn6.signal = True

sn10.signal = True
sn11.signal = True
sn12.signal = True
sn13.signal = True
sn14.signal = True
sn15.signal = True

# set of the environment
sns = [sn0, sn1, sn2, sn3, sn4, sn5, sn6, sn7, sn8, sn9, sn10, sn11, sn12, sn13, sn14, sn15]
trs = [tr0_1_8, tr1_2, tr2_3, tr3_4, tr4_5, tr5_6, tr7_6_15, tr8_9, tr9_10, tr10_11, tr11_12, tr12_13, tr13_14, tr14_15]
env1 = Environment('env1', trs, sns, [])
print(env1)

# set of the train(s)
position1 = Position(tr0_1_8, 60.)
# opt1 = Position(tr2_3, 30.)
train93341 = Train('93341', 50., position1, sn1)
# train93341 = Train('93341', 50., opt1, sn3)
train93341.print_train()

train36027 = Train('36027', 50., Position(tr7_6_15, 60.), sn15)
train36027.print_train()

measure93341 = Measure(train93341)
measure36027 = Measure(train36027)

dummy93341 = Dummy(measure93341)
dummy36027 = Dummy(measure36027)

time = 0.
dt = 0.1

dummy93341.state_set('RUN')
train93341.target_speed = 25.

TT = []
DD = []
VV = []
D2C = []
NVC = []
TV = []

while time < 30.5:
    TT.append(time)
    DD.append(train93341.head.abs_position_line)
    VV.append(dummy93341.speed)
    D2C.append(dummy93341.dis_2_change)
    NVC.append(dummy93341.next_speed)
    TV.append(dummy93341.target_speed)
    dummy93341.command(dt)
    # train93341.state['RUN'](dt)
    time += dt

# dummy93341.state_set('BRAKE')

while train93341.speed:
    TT.append(time)
    DD.append(train93341.head.abs_position_line)
    VV.append(dummy93341.speed)
    D2C.append(dummy93341.dis_2_change)
    NVC.append(dummy93341.next_speed)
    TV.append(dummy93341.target_speed)
    dummy93341.command(dt)
    # train93341.state['BRAKE'](dt)
    time += dt

TT.append(time)
DD.append(train93341.head.abs_position_line)
VV.append(dummy93341.speed)
D2C.append(dummy93341.dis_2_change)
NVC.append(dummy93341.next_speed)
TV.append(dummy93341.target_speed)
dummy93341.state_set()
dummy93341.command(dt)

dummy93341.print_dummy()

XX, YY = env1.lines[0].show_limit_speed_info()

# plt.figure(1)
# plt.plot(DD,VV,'b')
# plt.plot(DD,D2C,'y')
# plt.plot(DD,NVC,'r')
# plt.plot(XX,YY)

plt.figure(2)
plt.plot(DD,VV,'b')
plt.plot(XX,YY,'r')
plt.plot(DD,NVC,'g--')
plt.plot(DD,TV,'y--')
plt.xlabel('distance on the route')
plt.ylabel('speed (m/s)')
plt.legend(('speed', 'limit speed', 'next limit speed inf', 'current target speed'),
           loc=(0.30, 0.40), fontsize=8)
plt.title('a simple scenario of traffic simulation')

# plt.figure()
# plt.plot(DD,TV)
plt.savefig('illustration.png')
# plt.show()




