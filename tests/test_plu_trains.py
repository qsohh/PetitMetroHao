#!/usr/bin/env python
import sys
sys.path.append('./DefClass')

import matplotlib.pyplot as plt
import numpy as np

from def_line import Track, Node, signals2pass
from def_train import Position, Train
from def_measure import Measure
from def_dummy import Dummy
from def_environment import Environment, Balise
from def_station import Station, Terminus_v0

# set of the <Node>s
sns = []
for i in range(30):
    node_name = 'node_%02d' % i
    sns.append(Node(node_name))

# set of the <Track>s
trs = []
for i in range(7):
    track_name = 'track_%02d_%02d' % (i*4, i*4+1)
    trs.append(Track(track_name, 70., sns[i*4], sns[i*4+1], 5.))
    track_name = 'track_%02d_%02d' % (i*4+1, i*4+2)
    trs.append(Track(track_name, 200., sns[i*4+1], sns[i*4+2], 23.))
    track_name = 'track_%02d_%02d' % (i*4+2, i*4+3)
    trs.append(Track(track_name, 110., sns[i*4+2], sns[i*4+3], 20.))
    track_name = 'track_%02d_%02d' % (i*4+3, i*4+4)
    trs.append(Track(track_name, 55., sns[i*4+3], sns[i*4+4], 15.))
track_name = 'track_28_29'
trs.append(Track((track_name), 70., sns[28], sns[29], 5.))

# initial pass ginals
snpass = sns[1:4] + sns[6:9] + sns[10:13] + sns[14:17] + sns[18:21] + \
         sns[22:25] + sns[26:29]
signals2pass(snpass)

# set of the environment
env1 = Environment('env1', trs, sns, [])
print(env1)

# set of the <Balise>s
baps = []
bens = []
bnns = []
for i in range(6):
    ap_name = 'bap_%02d' % i
    en_name = 'ben_%02d' % i
    nn_name = 'bnn_%02d' % i
    baps.append(Balise(ap_name, Position(trs[i*4+2], 5.)))
    bens.append(Balise(en_name, Position(trs[i*4+3], 50.)))
    bnns.append(Balise(nn_name, Position(trs[i*4+5], 165.)))
ap_name = 'bap_06'
en_name = 'ben_06'
baps.append(Balise(ap_name, Position(trs[26], 5.)))
bens.append(Balise(en_name, Position(trs[27], 50.)))
env1.equipements = baps + bens + bnns

# set of the <Station>
stations = []
for i in range(6):
    station_name = 'station_%02d' % i
    stations.append(Station(station_name, trs[i*4+4], sns[i*4+4], sns[i*4+5],
                    baps[i], bens[i], bnns[i], sns[i*4+3]))
    stations[i].state = 'NN'
# stations.append(Terminus_v0('St-Remy-Les-Chevereuse', trs[28], sns[28],
#                 sns[29], baps[6], bens[6], sns[27]))
stations[-1].state = 'NN'

# set of the <Train>s
train93341 = Train('93341', 50., Position(trs[4], 60.), sns[5])
train95542 = Train('95542', 50., Position(trs[0], 60.), sns[1])
trains = [train93341, train95542]
env1.set_trains(trains)

# add the train to the passing train of the station
for ele in stations:
    ele.find_trains()
stations[0].state = 'ST'

# set the measure and the dummy
measures = []
dummies = []
for ele in trains:
    measures.append(Measure(ele))
    dummies.append(Dummy(measures[-1]))

TIME = 0.
dt = 0.05

dummies[0].state_set('STOP')
dummies[0].at_station = True
dummies[1].state_set('STOP')
dummies[1].at_station = True

for ele in dummies:
    ele.command(dt)
for ele in stations:
    ele.control(TIME, dt)

TT = []
TT.append(TIME)
TIME += dt

# while TIME < 8.:
# while True:
while TIME < 490.:  # 130.:
    TT.append(TIME)
    env1.update_env()
    for ele in dummies:
        ele.command(dt)
    for ele in stations:
        ele.control(TIME, dt)
    env1.update_env()
    # train93341.update_train()
    TIME += dt

# XX, YY = env1.lines[0].show_limit_speed_info()
# XX2, YY2 = env1.lines[1].show_limit_speed_info()
# for i in range(len(XX2)):
#     XX2[i] += env1.lines[0].tracklength_line  # 435.

# plt.figure()
# plt.plot(TT, train93341.VV)
# plt.xlabel('TIME (s)')
# plt.ylabel('speed (m/s)')
# plt.title('current speed of a simple scenario of traffic simulation')

# plt.figure()
# plt.plot(DD1, train93341.VV, 'b')
# # plt.plot(XX+XX2, YY+YY2, 'r')
# plt.plot(DD1, dummies[0].NVC, 'g--')
# plt.plot(DD1, train93341.TV, 'y--')
# # plt.axvline(x=275.)
# # plt.axvline(x=430.)
# # plt.axvline(x=165. + 505.)
# plt.xlabel('distance on the route (m)')
# plt.ylabel('speed (m/s)')
# plt.legend(('current speed',  # 'limit speed',
#            'next limit speed inf', 'current target speed'),
#            loc=(0.13, 0.05), fontsize=8)
# plt.title('a simple scenario of traffic simulation')
# # plt.savefig('2stations_v_d.png')

# set of the absolut position:
added_position = []
length = 0.
for ele in trs:
    added_position.append(length)
    length += ele.tracklength

D1 = []
D2 = []
for i in range(len(TT)):
    D1.append(added_position[trs.index(trains[0].PP[i].track)] +
              trains[0].PP[i].abs_position_track)
    D2.append(added_position[trs.index(trains[1].PP[i].track)] +
              trains[1].PP[i].abs_position_track)

plt.figure()
plt.plot(TT, D1, 'b')
plt.plot(TT, D2, 'r')
plt.title('test 2 trains')
plt.xlabel('time (s)')
plt.ylabel('position (m)')
# plt.savefig('2_trains.png')
plt.show()
