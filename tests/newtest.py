#!/usr/bin/env python
import sys
sys.path.append('./DefClass')

import matplotlib.pyplot as plt

from def_line import Track, Node, signals2pass
from def_train import Position, Train
from def_measure import Measure
from def_dummy import Dummy
from def_environment import Environment, Balise
from def_station import Station

# set of the <Node>s
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

# set of the <Track>s
tr0_1 = Track('tr0_1', 70., sn0, sn1, 5.)
tr1_2 = Track('tr1_2', 200., sn1, sn2, 28.)
tr2_3 = Track('tr2_3', 110., sn2, sn3, 20.)
tr3_4 = Track('tr3_4', 55., sn3, sn4, 15.)
tr4_5 = Track('tr4_5', 70., sn4, sn5, 5.)
tr5_6 = Track('tr5_6', 170., sn5, sn6, 28.)
tr6_7 = Track('tr6_7', 110., sn6, sn7, 20.)
tr7_8 = Track('tr7_8', 55., sn7, sn8, 15.)
tr8_9 = Track('tr8_9', 70., sn8, sn9, 5.)

# initial pass ginals
snpass = [sn1, sn2, sn3, sn4, sn6, sn7, sn8]
signals2pass(snpass)

# set of the environment
sns = [sn0, sn1, sn2, sn3, sn4, sn5, sn6, sn7, sn8, sn9]
trs = [tr0_1, tr1_2, tr2_3, tr3_4, tr4_5, tr5_6, tr6_7, tr7_8, tr8_9]
env1 = Environment('env1', trs, sns, [])
print(env1)

# set of the <Balise>s
ba1 = Balise('bap1', Position(tr2_3, 5.))
be1 = Balise('ben1', Position(tr3_4, 50.))
bn1 = Balise('bnn1', Position(tr5_6, 165.))

# set of the <Station>
station1 = Station('Port_Royal', tr4_5, sn4, sn5, ba1, be1, bn1, sn3)
station1.state = 'NN'

# set of the <Train>
train93341 = Train('93341', 50., Position(tr0_1, 60.), sn1)
train93341.print_train()

# add the train to the passing train of the station
station1.set_passing_train(train93341)