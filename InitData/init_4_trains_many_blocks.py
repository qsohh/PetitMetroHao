from DefClass.def_line import Track, Node, signals2pass, Junction
from DefClass.def_train import Position, Train
from DefClass.def_measure import Measure
from DefClass.def_dummy import Dummy
from DefClass.def_environment import Environment, Balise
from DefClass.def_station import Station, Terminus_v0

sns = []
for i in range(36):
    node_name = 'node_%02d' % i
    sns.append(Node(node_name))

# set of the <Track>s
trs = []
for i in range(2):
    track_name = 'track_%02d_%02d' % (i*18, i*18+1)
    trs.append(Track(track_name, 70., sns[i*18], sns[i*18+1], 5.))
    track_name = 'track_%02d_%02d' % (i*18+1, i*18+2)
    trs.append(Track(track_name, 30., sns[i*18+1], sns[i*18+2], 7.))
    track_name = 'track_%02d_%02d' % (i*18+2, i*18+3)
    trs.append(Track(track_name, 190., sns[i*18+2], sns[i*18+3], 23.))
    track_name = 'track_%02d_%02d' % (i*18+3, i*18+4)
    trs.append(Track(track_name, 200., sns[i*18+3], sns[i*18+4], 23.))
    track_name = 'track_%02d_%02d' % (i*18+4, i*18+5)
    trs.append(Track(track_name, 100., sns[i*18+4], sns[i*18+5], 15.))
    track_name = 'track_%02d_%02d' % (i*18+5, i*18+6)
    if i == 0:
        trs.append(Track(track_name, 100., sns[i*18+5], sns[i*18+6], 23.))
    else:
        trs.append(Track(track_name, 200., sns[i*18+5], sns[i*18+6], 23.))
    track_name = 'track_%02d_%02d' % (i*18+6, i*18+7)
    if i == 0:
        trs.append(Track(track_name, 100., sns[i*18+6], sns[i*18+7], 23.))
    else:
        trs.append(Track(track_name, 200., sns[i*18+6], sns[i*18+7], 23.))
    track_name = 'track_%02d_%02d' % (i*18+7, i*18+8)
    trs.append(Track(track_name, 110., sns[i*18+7], sns[i*18+8], 20.))
    track_name = 'track_%02d_%02d' % (i*18+8, i*18+9)
    trs.append(Track(track_name, 55., sns[i*18+8], sns[i*18+9], 15.))
    track_name = 'track_%02d_%02d' % (i*18+9, i*18+10)
    trs.append(Track(track_name, 70., sns[i*18+9], sns[i*18+10], 5.))
    track_name = 'track_%02d_%02d' % (i*18+10, i*18+11)
    trs.append(Track(track_name, 200., sns[i*18+10], sns[i*18+11], 23.))
    track_name = 'track_%02d_%02d' % (i*18+11, i*18+12)
    trs.append(Track(track_name, 200., sns[i*18+11], sns[i*18+12], 23.))
    track_name = 'track_%02d_%02d' % (i*18+12, i*18+13)
    trs.append(Track(track_name, 100., sns[i*18+12], sns[i*18+13], 15.))
    track_name = 'track_%02d_%02d' % (i*18+13, i*18+14)
    if i == 1:
        trs.append(Track(track_name, 100., sns[i*18+13], sns[i*18+14], 23.))
    else:
        trs.append(Track(track_name, 200., sns[i*18+13], sns[i*18+14], 23.))
    track_name = 'track_%02d_%02d' % (i*18+14, i*18+15)
    if i == 1:
        trs.append(Track(track_name, 100., sns[i*18+14], sns[i*18+15], 23.))
    else:
        trs.append(Track(track_name, 200., sns[i*18+14], sns[i*18+15], 23.))
    track_name = 'track_%02d_%02d' % (i*18+15, i*18+16)
    trs.append(Track(track_name, 110., sns[i*18+15], sns[i*18+16], 20.))
    track_name = 'track_%02d_%02d' % (i*18+16, i*18+17)
    trs.append(Track(track_name, 55., sns[i*18+16], sns[i*18+17], 15.))

# prepare to set the joinctions
sns[17].list_tracks_node.append(trs[17])
sns[35].list_tracks_node.append(trs[0])

# set of the joinctions
jcts = []
jcts.append(Junction('Jct_St-Remy', sns[1], sns[35]))
jcts.append(Junction('Jct_CDG', sns[17], sns[19]))

# initial pass ginals
# snpass = sns[1:6] + sns[7:9] + sns[12:16] + [sns[17]]
# signals2pass(snpass)

# set of the environment
env1 = Environment('env1', trs, sns, [])
jcts[0].switch_to(sns[1])
jcts[1].switch_to(sns[19])
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
    baps.append(Balise(ap_name, Position(trs[i*17-2], 5.)))
    bens.append(Balise(en_name, Position(trs[i*17-1], 50.)))
    bnns.append(Balise(nn_name, Position(trs[i*17+2], 35.)))
    ap_name = 'bap_%02d' % (i*2+1)
    en_name = 'ben_%02d' % (i*2+1)
    nn_name = 'bnn_%02d' % (i*2+1)
    baps.append(Balise(ap_name, Position(trs[i*17+7], 5.)))
    bens.append(Balise(en_name, Position(trs[i*17+8], 50.)))
    bnns.append(Balise(nn_name, Position(trs[i*17+10], 65.)))
env1.equipements = baps + bens + bnns

# for ele in env1.equipements:
#     print(ele)

# set of the <Station>
stations = []
for i in range(2):
    station_name = 'station_%02d' % (i*2)
    stations.append(Terminus_v0(station_name, trs[i*17], sns[i*18-1],
                    sns[i*18+1], sns[i*18], baps[i*2], bens[i*2], bnns[i*2],
                    sns[i*18-2], jcts[i]))
    stations[i*2].state = 'NN'
    stations[i*2].signal_ap.signal_stop()
    station_name = 'station_%02d' % (i*2+1)
    stations.append(Station(station_name, trs[i*17+9], sns[i*18+9], sns[i*18+10],
                    baps[i*2+1], bens[i*2+1], bnns[i*2+1], sns[i*18+8]))
    stations[i*2+1].state = 'NN'
    stations[i*2+1].signal_ap.signal_stop()

# set of the <Train>s
train00 = Train('00', 50., Position(trs[0], 60.), sns[1])
train01 = Train('01', 50., Position(trs[9], 60.), sns[10])
train02 = Train('02', 50., Position(trs[17], 60.), sns[19])
train03 = Train('03', 50., Position(trs[26], 60.), sns[28])
trains = [train00, train01, train02, train03]
env1.set_trains(trains)

# add the train to the passing train of the station
for ele in stations:
    ele.find_trains()
stations[0].set_passing_train(train00, 0.)
stations[0].state = 'ST'
stations[1].set_passing_train(train01, 0.)
stations[1].state = 'ST'
stations[2].set_passing_train(train02, 0.)
stations[2].state = 'ST'
stations[3].set_passing_train(train03, 0.)
stations[3].state = 'ST'


# set the measure and the dummy
measures = []
dummies = []
for ele in trains:
    measures.append(Measure(ele))
    dummies.append(Dummy(measures[-1]))
    dummies[-1].state_set('STOP')
    dummies[-1].at_station = True

TIME = 0.
dt = 0.1
