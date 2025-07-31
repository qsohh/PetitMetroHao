from DefClass.def_line import Track, Node, signals2pass, Junction
from DefClass.def_train import Position, Train
from DefClass.def_measure import Measure
from DefClass.def_dummy import Dummy
from DefClass.def_environment import Environment, Balise
from DefClass.def_station import Station, Terminus_v0

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
    if i == 0:
        trs.append(Track(track_name, 190.+500., sns[i*10+2], sns[i*10+3], 23.))
    else:
        trs.append(Track(track_name, 190.+700., sns[i*10+2], sns[i*10+3], 23.))
    track_name = 'track_%02d_%02d' % (i*10+3, i*10+4)
    trs.append(Track(track_name, 110., sns[i*10+3], sns[i*10+4], 20.))
    track_name = 'track_%02d_%02d' % (i*10+4, i*10+5)
    trs.append(Track(track_name, 55., sns[i*10+4], sns[i*10+5], 15.))
    track_name = 'track_%02d_%02d' % (i*10+5, i*10+6)
    trs.append(Track(track_name, 70., sns[i*10+5], sns[i*10+6], 5.))
    track_name = 'track_%02d_%02d' % (i*10+6, i*10+7)
    if i == 1:
        trs.append(Track(track_name, 200.+500., sns[i*10+6], sns[i*10+7], 23.))
    else:
        trs.append(Track(track_name, 200.+700., sns[i*10+6], sns[i*10+7], 23.))
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
snpass = sns[1:6] + sns[7:9] + sns[12:16] + [sns[17]]
signals2pass(snpass)

# set of the environment
env1 = Environment('env1', trs, sns, [])
jcts[0].switch_to(sns[1])
jcts[1].switch_to(sns[11])
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
    bnns.append(Balise(nn_name, Position(trs[i*9+2], 35.)))
    ap_name = 'bap_%02d' % (i*2+1)
    en_name = 'ben_%02d' % (i*2+1)
    nn_name = 'bnn_%02d' % (i*2+1)
    baps.append(Balise(ap_name, Position(trs[i*9+3], 5.)))
    bens.append(Balise(en_name, Position(trs[i*9+4], 50.)))
    bnns.append(Balise(nn_name, Position(trs[i*9+6], 65.)))
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
train00 = Train('00', 50., Position(trs[0], 60.), sns[1])
train01 = Train('01', 50., Position(trs[5], 60.), sns[6])
train02 = Train('02', 50., Position(trs[9], 60.), sns[11])
train03 = Train('03', 50., Position(trs[14], 60.), sns[16])

train04 = Train('04', 50., Position(trs[2], 500.), sns[3])
train05 = Train('05', 50., Position(trs[6], 500.), sns[7])
train06 = Train('06', 50., Position(trs[11], 500.), sns[13])
ttrains = [train00, train01, train02, train03,
           train04, train05, train06]

OrTra = [0, 4, 1, 5, 2, 6, 3]
trains = []
for i in range(len(ttrains)):
    trains.append(ttrains[OrTra[i]])
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

for i in [1, 3, 5]:
    dummies[i].at_station = False


TIME = 0.
dt = 0.1
