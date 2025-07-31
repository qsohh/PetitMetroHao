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
sn16 = Node('sn16')

tr0_1 = Track('tr1_2', 70., sn0, sn1, 5.)
tr1_2 = Track('tr1_2', 20., sn1, sn2, 20.)  # 20.)
tr2_3 = Track('tr2_3', 200., sn2, sn3, 30.)
tr3_4 = Track('tr3_4', 100., sn3, sn4, 30.)
tr4_5 = Track('tr4_5', 60., sn4, sn5, 28.)
tr5_6 = Track('tr5_6', 120., sn5, sn6, 30.)
tr6_7 = Track('tr6_7', 150., sn6, sn7, 25.)
tr7_8 = Track('tr7_8', 110., sn7, sn8, 25.)
tr8_9 = Track('tr8_9', 80., sn8, sn9, 25.)
tr9_10 = Track('tr9_10', 100., sn9, sn10, 30.)
tr10_11 = Track('tr10_11', 300., sn10, sn11, 30.)
tr11_12 = Track('tr11_12', 100., sn11, sn12, 20.)
tr12_13 = Track('tr12_13', 80., sn12, sn13, 30.)
tr13_14 = Track('tr13_14', 120., sn13, sn14, 30.)
tr14_15 = Track('tr14_15', 60., sn14, sn15, 30.)
tr15_16 = Track('tr15_16', 70., sn15, sn16, 5.)

sn1.signal = True
sn2.signal = True
sn3.signal = True
sn4.signal = True
sn5.signal = True
sn6.signal = True
sn7.signal = True
sn8.signal = True
sn9.signal = True
sn10.signal = True
sn11.signal = True
sn12.signal = True
sn13.signal = True
sn14.signal = True
sn15.signal = True

sns = [sn0, sn1, sn2, sn3, sn4, sn5, sn6, sn7, sn8, sn9, sn10, sn11, sn12, sn13, sn14, sn15, sn16]
trs = [tr0_1, tr1_2, tr2_3, tr3_4, tr4_5, tr5_6, tr6_7, tr7_8, tr8_9, tr9_10, tr10_11, tr11_12, tr12_13, tr13_14, tr14_15, tr15_16]
env1 = Environment('env1', trs, sns, [])
print(env1)

train93341 = Train('93341', 50., Position(tr0_1, 60.), sn1)
train93341.print_train()

measure93341 = Measure(train93341)
dummy93341 = Dummy(measure93341)

time = 0.
dt = 0.1

dummy93341.state_set('RUN')
dummy93341.command(dt)

TT = []
DD = []
VV = []
D2C = []
NVC = []
TV = []

TT.append(time)
DD.append(train93341.head.abs_position_line)
VV.append(dummy93341.speed)
D2C.append(dummy93341.dis_2_change)
NVC.append(dummy93341.next_speed)
TV.append(dummy93341.target_speed)
dummy93341.command(dt)
time += dt

while train93341.speed:
    TT.append(time)
    DD.append(train93341.head.abs_position_line)
    VV.append(dummy93341.speed)
    D2C.append(dummy93341.dis_2_change)
    NVC.append(dummy93341.next_speed)
    TV.append(dummy93341.target_speed)
    dummy93341.command(dt)
    time += dt

TT.append(time)
DD.append(train93341.head.abs_position_line)
VV.append(dummy93341.speed)
D2C.append(dummy93341.dis_2_change)
NVC.append(dummy93341.next_speed)
TV.append(dummy93341.target_speed)
dummy93341.state_set('STOP')
dummy93341.command(dt)

dummy93341.print_dummy()

XX, YY = env1.lines[0].show_limit_speed_info()


plt.figure()
plt.plot(DD, VV, 'b')
plt.plot(XX, YY, 'r')
plt.plot(DD, NVC, 'g--')
plt.plot(DD, TV, 'y--')
plt.xlabel('distance on the route')
plt.ylabel('speed (m/s)')
plt.legend(('speed', 'limit speed', 'next limit speed inf', 'current target speed'),
           loc=(0.30, 0.40), fontsize=8)
plt.title('a simple scenario of traffic simulation')
plt.show()
# plt.savefig('ex_simulation.png')
