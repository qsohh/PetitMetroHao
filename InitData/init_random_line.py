from DefClass.def_line import Track, Node, signals2pass, Junction
from DefClass.def_train import Position, Train
from DefClass.def_measure import Measure
from DefClass.def_dummy import Dummy
from DefClass.def_environment import Environment, Balise
from DefClass.def_station import Station, Terminus_v0
from Generator.gen_line import gen_line_averange_ver0, test_track_name

number_stations = 4
m = 2
# test_track_name(number_stations, m)

sns, trs, jcts, env, stations = gen_line_averange_ver0(1800., 4)

print(env)
