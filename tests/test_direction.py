#!/usr/bin/env python
import sys
sys.path.append('./DefClass')

import matplotlib.pyplot as plt

from def_line import Track, Node, signals2pass, Junction
from def_train import Position, Train
from def_measure import Measure
from def_dummy import Dummy
from def_environment import Environment, Balise
from def_station import Station, Terminus_v0

# set of the <Node>s
sns = []
for i in range(5):
    node_name = 'node_%02d' % i
    sns.append(Node(node_name))

# set of the <Track>s
trs = []
for i in range(4):
    track_name = 'track_%02d_%02d' % (i, i+1)
    trs.append(Track(track_name, 70., sns[i], sns[i+1], 5.))

# initial pass ginals
snpass = sns[1:5]
signals2pass(snpass)

# set of the environment
env1 = Environment('env1', trs, sns, [])
env1.update_env()
print(env1)

trs[0].switch_direction()

env1.update_env()
print(env1)
# ---------------------------------------------------------------
