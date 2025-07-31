#!/usr/bin/env python
# import sys
# sys.path.append('./DefClass')

import matplotlib.pyplot as plt

from DefClass.def_line import Track, Node, signals2pass, Junction
from DefClass.def_train import Position, Train
from DefClass.def_measure import Measure
from DefClass.def_dummy import Dummy
from DefClass.def_environment import Environment, Balise
from DefClass.def_station import Station, Terminus_v0

# set of the <Node>s
sns = []
for i in range(20):
    node_name = 'node_%02d' % i
    sns.append(Node(node_name))

# set of the <Track>s
trs = []
for i in range(2):
    track_name = 'track_%02d_%02d' % (i*10, i*10+1)
    trs.append(Track(track_name, 70., sns[i*10], sns[i*10+1], 5.))
    track_name = 'track_%02d_%02d' % (i*10+1, i*10+2)
    trs.append(Track(track_name, 30., sns[i*10+1], sns[i*10+2], 7.))
    track_name = 'track_%02d_%02d' % (i*10+2, i*10+3)
    trs.append(Track(track_name, 190., sns[i*10+2], sns[i*10+3], 23.))
    track_name = 'track_%02d_%02d' % (i*10+3, i*10+4)
    trs.append(Track(track_name, 110., sns[i*10+3], sns[i*10+4], 20.))
    track_name = 'track_%02d_%02d' % (i*10+4, i*10+5)
    trs.append(Track(track_name, 55., sns[i*10+4], sns[i*10+5], 15.))
    track_name = 'track_%02d_%02d' % (i*10+5, i*10+6)
    trs.append(Track(track_name, 70., sns[i*10+5], sns[i*10+6], 5.))
    track_name = 'track_%02d_%02d' % (i*10+6, i*10+7)
    trs.append(Track(track_name, 200., sns[i*10+6], sns[i*10+7], 23.))
    track_name = 'track_%02d_%02d' % (i*10+7, i*10+8)
    trs.append(Track(track_name, 110., sns[i*10+7], sns[i*10+8], 20.))
    track_name = 'track_%02d_%02d' % (i*10+8, i*10+9)
    trs.append(Track(track_name, 55., sns[i*10+8], sns[i*10+9], 15.))

# prepare to set the joinctions
sns[9].list_tracks_node.append(trs[9])
sns[19].list_tracks_node.append(trs[0])

# set of the joinctions
jcts = []
jcts.append(Junction('Jct_St-Remy', sns[1], sns[19]))
jcts.append(Junction('Jct_CDG', sns[9], sns[11]))

# initial pass ginals
snpass = sns[1:6] + sns[7:10] + sns[12:16] + [sns[17]]
signals2pass(snpass)

# set of the environment
env1 = Environment('env1', trs, sns, [])
jcts[0].switch_to(sns[1])
jcts[1].switch_from(sns[9])
env1.update_env()
# print(env1)

# set of the <Balise>s
baps = []
bens = []
bnns = []
for i in range(2):
    ap_name = 'bap_%02d' % (i*2)
    en_name = 'ben_%02d' % (i*2)
    nn_name = 'bnn_%02d' % (i*2)
    baps.append(Balise(ap_name, Position(trs[i*9-2], 5.)))
    bens.append(Balise(en_name, Position(trs[i*9-1], 50.)))
    bnns.append(Balise(nn_name, Position(trs[i*9+2], 135.)))
    ap_name = 'bap_%02d' % (i*2+1)
    en_name = 'ben_%02d' % (i*2+1)
    nn_name = 'bnn_%02d' % (i*2+1)
    baps.append(Balise(ap_name, Position(trs[i*9+3], 5.)))
    bens.append(Balise(en_name, Position(trs[i*9+4], 50.)))
    bnns.append(Balise(nn_name, Position(trs[i*9+6], 165.)))
env1.equipements = baps + bens + bnns

# for ele in env1.equipements:
#     print(ele)

# set of the <Station>
stations = []
for i in range(2):
    station_name = 'station_%02d' % (i*2)
    stations.append(Terminus_v0(station_name, trs[i*9], sns[i*10-1],
                    sns[i*10+1], sns[i*10], baps[i*2], bens[i*2], bnns[i*2],
                    sns[i*10-2], jcts[i]))
    stations[i*2].state = 'NN'
    station_name = 'station_%02d' % (i*2+1)
    stations.append(Station(station_name, trs[i*9+5], sns[i*10+5], sns[i*10+6],
                    baps[i*2+1], bens[i*2+1], bnns[i*2+1], sns[i*10+4]))
    stations[i*2+1].state = 'NN'

# set of the <Train>s
train93341 = Train('93341', 50., Position(trs[0], 60.), sns[1])
trains = [train93341]
env1.set_trains(trains)

TIME = 0.
dt = 0.1

# add the train to the passing train of the station
for ele in stations:
    ele.find_trains()
stations[0].set_passing_train(train93341, TIME)
stations[0].state = 'ST'

# set the measure and the dummy
measures = []
dummies = []
for ele in trains:
    measures.append(Measure(ele))
    dummies.append(Dummy(measures[-1]))

dummies[0].state_set('STOP')
dummies[0].at_station = True

for ele in dummies:
    ele.command(dt)
for ele in stations:
    ele.control(TIME, dt)

TT = []
TT.append(TIME)
TIME += dt

# ---------------------------------------------------------------

while TIME < 700.:  # 130.:
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
for ele in trs[0:10]:
    added_position.append(length)
    length += ele.tracklength
length -= 70.
for ele in trs[10:]:
    added_position.append(length)
    length -= ele.tracklength
added_position[9] += 70.
# ad = added_position[:]
# added_position[-1] += 70.
# while ad:
#     added_position.append(ad.pop())

new_p = [0., 70., 100., 290., 400., 455., 525., 725., 835., 960., 890., 835.,
         725., 525., 455., 400., 290., 100., 70.]

D1 = []
D2 = []
for i in range(len(TT)):
    ind = trs.index(trains[0].PP[i].track)
    if ind < 9:
        D1.append(added_position[ind] + trains[0].PP[i].abs_position_track)
        D2.append(new_p[ind] + trains[0].PP[i].abs_position_track)
    else:
        D1.append(added_position[ind] - trains[0].PP[i].abs_position_track)
        D2.append(new_p[ind] - trains[0].PP[i].abs_position_track)


plt.figure()
plt.plot(TT, D1, 'b')
# plt.plot(TT, D2, 'r')
plt.xlabel('time (s)')
plt.ylabel('position (m)')
plt.title('two terminus')
# plt.savefig('2_terminus.png')
plt.show()
