#!/usr/bin/env python
import sys
sys.path.append('./DefClass')

import matplotlib.pyplot as plt

from def_line import Track
# from def_line import Line
from def_line import Node
from def_line import signals2pass
# from def_line import signals2stop
from def_train import Train
from def_train import Position
# from def_center import Center
from def_measure import Measure
from def_dummy import Dummy
from def_environment import Environment

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

sn17 = Node('sn17')
sn18 = Node('sn18')
sn19 = Node('sn19')
sn20 = Node('sn20')
sn21 = Node('sn21')
sn22 = Node('sn22')

tr0_1 = Track('tr0_1', 70., sn0, sn1, 5.)
tr1_2 = Track('tr1_2', 20., sn1, sn2, 20.)
tr2_3 = Track('tr2_3', 200., sn2, sn3, 30.)
tr3_4 = Track('tr3_4', 100., sn3, sn4, 30.)
tr4_5 = Track('tr4_5', 60., sn4, sn5, 28.)
tr5_6 = Track('tr5_6', 120., sn5, sn6, 30.)
tr6_7 = Track('tr6_7', 150., sn6, sn7, 25.)
tr7_8 = Track('tr7_8', 110., sn7, sn8, 25.)
tr8_9 = Track('tr8_9', 70., sn8, sn9, 5.)
tr9_10 = Track('tr9_10', 100., sn9, sn10, 30.)
tr10_11 = Track('tr10_11', 300., sn10, sn11, 30.)
tr11_12 = Track('tr11_12', 100., sn11, sn12, 20.)
tr12_13 = Track('tr12_13', 80., sn12, sn13, 30.)
tr13_14 = Track('tr13_14', 120., sn13, sn14, 30.)
tr14_15 = Track('tr14_15', 60., sn14, sn15, 30.)
tr15_16 = Track('tr15_16', 70., sn15, sn16, 5.)

tr16_17 = Track('tr16_17', 700., sn16, sn17, 25.)
tr17_18 = Track('tr17_18', 70., sn17, sn18, 5.)
tr18_19 = Track('tr18_19', 700., sn18, sn19, 25.)
tr19_20 = Track('tr19_20', 70., sn19, sn20, 5.)
tr20_21 = Track('tr20_21', 700., sn20, sn21, 25.)
tr21_22 = Track('tr21_22', 70., sn21, sn22, 5.)

# sn1.signal = True
# sn2.signal = True
# sn3.signal = True
# sn4.signal = True
# sn5.signal = True
# sn6.signal = True
# sn7.signal = True
# sn8.signal = True
# sn9.signal = False
# sn10.signal = True
# sn11.signal = True
# sn12.signal = True
# sn13.signal = True
# sn14.signal = True
# sn15.signal = True

snpass = [sn1, sn2, sn3, sn4, sn5, sn6, sn7, sn8, sn10, sn11, sn12, sn13,
          sn14, sn15, sn17, sn19, sn21]
signals2pass(snpass)

sns = [sn0, sn1, sn2, sn3, sn4, sn5, sn6, sn7, sn8, sn9, sn10, sn11, sn12,
       sn13, sn14, sn15, sn16, sn17, sn18, sn19, sn20, sn21, sn22]
trs = [tr0_1, tr1_2, tr2_3, tr3_4, tr4_5, tr5_6, tr6_7, tr7_8, tr8_9, tr9_10,
       tr10_11, tr11_12, tr12_13, tr13_14, tr14_15, tr15_16,
       tr16_17, tr17_18, tr18_19, tr19_20, tr20_21, tr21_22]
env1 = Environment('env1', trs, sns, [])
print(env1)
env1.report_track_number_line1()

train93341 = Train('93341', 50., Position(tr0_1, 60.), sn1)
env1.report_track_number_line1()
train93341.print_train()

measure93341 = Measure(train93341)
dummy93341 = Dummy(measure93341)
env1.report_track_number_line1()

time = 0.
dt = 0.1

dummy93341.state_set('RUN')
dummy93341.command(dt)
env1.report_track_number_line1()

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
env1.report_track_number_line1()
dummy93341.command(dt)
time += dt

print(env1)

# while time < 8.:
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

sn8.signal = False
sn9.signal = True
env1.update_env()

train93341.update_train()
print('time %f\n' % (time), env1)
env1.report_track_number_line1()
dummy93341.state_set('RUN')
time = time + 30

TT.append(time)
DD.append(train93341.head.abs_position_line + 830.)
VV.append(dummy93341.speed)
D2C.append(dummy93341.dis_2_change)
NVC.append(dummy93341.next_speed)
TV.append(dummy93341.target_speed)
env1.report_track_number_line1()
dummy93341.command(dt)
time += dt

while train93341.speed:
    TT.append(time)
    DD.append(train93341.head.abs_position_line + 830.)
    VV.append(dummy93341.speed)
    D2C.append(dummy93341.dis_2_change)
    NVC.append(dummy93341.next_speed)
    TV.append(dummy93341.target_speed)
    dummy93341.command(dt)
    time += dt

print(env1)

TT.append(time)
print(TT[-1])
DD.append(train93341.head.abs_position_line + 830.)
VV.append(dummy93341.speed)
D2C.append(dummy93341.dis_2_change)
NVC.append(dummy93341.next_speed)
TV.append(dummy93341.target_speed)
dummy93341.state_set()
dummy93341.command(dt)

dummy93341.print_dummy()

XX, YY = env1.lines[0].show_limit_speed_info()
XX2, YY2 = env1.lines[1].show_limit_speed_info()
for i in range(len(XX2)):
    XX2[i] += 830.
# plt.figure()
# plt.plot(TT,DD)

plt.figure()
plt.plot(TT, VV)
plt.xlabel('time (s)')
plt.ylabel('speed (m/s)')
plt.title('current speed of a simple scenario of traffic simulation')
# plt.savefig('2stations_v_t.png')

plt.figure()
plt.plot(DD, VV, 'b')
plt.plot(XX + XX2, YY + YY2, 'r')
plt.plot(DD, NVC, 'g--')
plt.plot(DD, TV, 'y--')
plt.xlabel('distance on the route (m)')
plt.ylabel('speed (m/s)')
plt.legend(('current speed', 'limit speed', 'next limit speed inf', 'current \
target speed'), loc=(0.13, 0.05), fontsize=8)
plt.title('a simple scenario of traffic simulation')
plt.show()
# plt.savefig('2stations_v_d.png')
