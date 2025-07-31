import numpy as np

from DefClass.def_line import Track, Node, signals2pass, Junction
from DefClass.def_error import FonctionError, StateError
from DefClass.def_train import Position
from DefClass.def_environment import Environment, Balise
from DefClass.def_station import Terminus_v0, Station


def gen_line_averange_ver0(totle_length: float, number_stations: int):
    '''
example of calling:
totle_length = 1800.
number_stations = 4
sns, trs, jcts, env, stations = gen_line_averange_ver0(totle_length,
                                                       number_stations)
    '''
    # n stations
    # 2*n-2 plateforms
    #
    aver_distance = (totle_length-number_stations*70.) / (number_stations-1)
    if aver_distance < 255.:
        raise ValueError('in fct |gen_line_averange_ver0|, too many stations \
within a too short totle length')
    if number_stations < 2:
        raise ValueError('in fct |gen_line_averange_ver0|, at least two \
stations are needed')
    if number_stations == 2:
        raise FonctionError('in fct |gen_line_averange_ver0|, the situation \
of two stations waiting to be added')
    if aver_distance < 420.:
        m = 0
    else:
        m = round((aver_distance - 255.) / 200.)
        if m == 0:
            raise FonctionError('in fct |gen_line_averange_ver0|, most \
strange error')
    # the number of the nodes
    number_node = 2+4+2*(2*(number_stations-2)+(2+m)*(number_stations-1))+2

    # set of the nodes
    sns = []
    for i in range(number_node):
        node_name = 'node_%02d' % i
        sns.append(Node(node_name))

    if m == 0:
        raise FonctionError('in fct |gen_line_averange_ver0|, the situation \
of m=0 waiting to be added')
    else:
        pass

    # generate the random lengths
    sigma_m2 = 0.36 * (aver_distance-255.)/(4*m)
    l_m = np.random.normal(0, sigma_m2, [(number_stations-1), m])
    llm = l_m - np.mean(l_m)
    length_variable = llm + (aver_distance - 255.)/m

    # generate the tracks
    trs = []
    nn2 = 1+2+(2*(number_stations-2)+(2+m)*(number_stations-1))+1
    for i in range(2):
        track_name = 'track_%02d_%02d' % (i*nn2, i*nn2+1)
        trs.append(Track(track_name, 70., sns[i*nn2], sns[i*nn2+1], 5.))
        track_name = 'track_%02d_%02d' % (i*nn2+1, i*nn2+2)
        trs.append(Track(track_name, 30., sns[i*nn2+1], sns[i*nn2+2], 7.))
        track_name = 'track_%02d_%02d' % (i*nn2+2, i*nn2+3)
        # on this track of length 70+20-30., the balise_nn
        trs.append(Track(track_name, 60., sns[i*nn2+2], sns[i*nn2+3], 23.))
        for k in range(m):
            track_name = 'track_%02d_%02d' % (i*nn2+3+k, i*nn2+4+k)
            if i == 0:
                ind = k
            else:
                ind = - k - 1
            trs.append(Track(track_name, length_variable[-i][ind],
                       sns[i*nn2+3+k], sns[i*nn2+4+k], 23.))
        track_name = 'track_%02d_%02d' % (i*nn2+m+3, i*nn2+m+4)
        # on this track of length 130., the balise_ap
        trs.append(Track(track_name, 130.,
                         sns[i*nn2+m+3], sns[i*nn2+m+4], 20.))
        track_name = 'track_%02d_%02d' % (i*nn2+m+4, i*nn2+m+5)
        # on this track of length 55., the balise_en
        trs.append(Track(track_name, 55., sns[i*nn2+m+4], sns[i*nn2+m+5], 15.))
        for j in range(1, number_stations-1):
            track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*j+1, i*nn2+(m+4)*j+2)
            trs.append(Track(track_name, 70., sns[i*nn2+(m+4)*j+1],
                             sns[i*nn2+(m+4)*j+2], 5.))
            track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*j+2, i*nn2+(m+4)*j+3)
            # on this track of length 70+20-30., the balise_nn
            trs.append(Track(track_name, 90., sns[i*nn2+(m+4)*j+2],
                             sns[i*nn2+(m+4)*j+3], 23.))
            if i == 0:
                ind1 = j
            else:
                ind1 = - j - 1
            for k in range(m):
                track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*j+3+k,
                                                  i*nn2+(m+4)*j+4+k)
                if i == 0:
                    ind2 = k
                else:
                    ind2 = - k - 1
                trs.append(Track(track_name, length_variable[ind1][ind2],
                                 sns[i*nn2+(m+4)*j+3+k],
                                 sns[i*nn2+(m+4)*j+4+k], 23.))
            track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*(j+1)-1,
                                              i*nn2+(m+4)*(j+1))
            # on this track of length 130., the balise_ap
            trs.append(Track(track_name, 130., sns[i*nn2+(m+4)*(j+1)-1],
                             sns[i*nn2+(m+4)*(j+1)], 20.))
            track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*(j+1),
                                              i*nn2+(m+4)*(j+1)+1)
            # on this track of length 55., the balise_en
            trs.append(Track(track_name, 55., sns[i*nn2+(m+4)*(j+1)],
                             sns[i*nn2+(m+4)*(j+1)+1], 20.))

    # prepare to generate the joinctions
    sns[nn2-1].list_tracks_node.append(trs[nn2-1])
    sns[-1].list_tracks_node.append(trs[0])

    # generate the two terminus joinctions
    jcts = []
    jcts.append(Junction('Jct_St-Remy', sns[1], sns[-1]))
    jcts.append(Junction('Jct_CDG', sns[nn2-1], sns[nn2+1]))

    # generate the environment
    env = Environment('env1', trs, sns, [])
    jcts[0].switch_to(sns[1])
    jcts[1].switch_to(sns[nn2+1])
    # env.update_env()

    # generate the <Balise>s
    baps = []
    bens = []
    bnns = []
    for i in range(2):
        ap_name = 'bap_%02d' % (i*(number_stations-1))
        en_name = 'ben_%02d' % (i*(number_stations-1))
        nn_name = 'bnn_%02d' % (i*(number_stations-1))
        baps.append(Balise(ap_name, Position(trs[i*(nn2-1)-2], 5.)))
        bens.append(Balise(en_name, Position(trs[i*(nn2-1)-1], 50.)))
        bnns.append(Balise(nn_name, Position(trs[i*(nn2-1)+2], 35.)))
        for j in range(1, number_stations-1):
            ap_name = 'bap_%02d' % (i*(number_stations-1)+j)
            en_name = 'ben_%02d' % (i*(number_stations-1)+j)
            nn_name = 'bnn_%02d' % (i*(number_stations-1)+j)
            baps.append(Balise(ap_name, Position(trs[i*(nn2-1)-2], 5.)))
            bens.append(Balise(en_name, Position(trs[i*(nn2-1)-1], 50.)))
            bnns.append(Balise(nn_name, Position(trs[i*(nn2-1)+2], 65.)))

    # generate the <Station>s
    stations = []
    for i in range(2):
        station_name = 'terminus_station_%02d' % (i*(number_stations-1))
        stations.append(Terminus_v0(station_name, trs[i*nn2-1],
                        sns[i*nn2-1], sns[i*nn2+1], sns[i*nn2],
                        baps[i*2], bens[i*2], bnns[i*2],
                        sns[i*nn2-2], jcts[i]))
        stations[-1].state = 'NN'
        stations[-1].signal_ap.signal_stop()
        for j in range(1, number_stations-1):
            station_name = 'station_%02d' % (i*(number_stations-1)+j)
            stations.append(Station(station_name, trs[i*(nn2-1)+(m+4)*j+1],
                            sns[i*nn2+(m+4)*j+1], sns[i*nn2+(m+4)*j+2],
                            baps[i*(number_stations-1)+j],
                            bens[i*(number_stations-1)+j],
                            bnns[i*(number_stations-1)+j],
                            sns[i*nn2+(m+4)*j-1]))
            stations[-1].state = 'NN'
            stations[-1].exit.signal_stop()

    # final update of the environment
    env.update_env()

    # report the generation of the line
    msg = 'Environment generated:\n'
    msg += '%d plateforms\n' % (2*number_stations-2)
    msg += 'with m = %d and aver_distance %7.f' % (m, aver_distance)
    print(msg)
    return sns, trs, jcts, env, stations


def test_track_name(number_stations, m):
    '''
    fct used for test the track_name
    m calculated by the method in the fct |gen_line_averange_ver0|
    '''
    number_node = 2+4+2*(2*(number_stations-2)+(2+m)*(number_stations-1))+2
    print('number of nodes: ', number_node)
    nn2 = 1+2+(2*(number_stations-2)+(2+m)*(number_stations-1))+1
    for i in range(2):
        track_name = 'track_%02d_%02d' % (i*nn2, i*nn2+1)
        print(track_name, i, 'j', 'k')
        track_name = 'track_%02d_%02d' % (i*nn2+1, i*nn2+2)
        print(track_name, i, 'j', 'k')
        track_name = 'track_%02d_%02d' % (i*nn2+2, i*nn2+3)
        print(track_name, i, 'j', 'k')
        for k in range(m):
            track_name = 'track_%02d_%02d' % (i*nn2+3+k, i*nn2+4+k)
            print(track_name, i, 'j', k)
        track_name = 'track_%02d_%02d' % (i*nn2+m+3, i*nn2+m+4)
        print(track_name, i, 'j', 'k')
        track_name = 'track_%02d_%02d' % (i*nn2+m+4, i*nn2+m+5)
        print(track_name, i, 'j', 'k')
        for j in range(1, number_stations-1):
            track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*j+1, i*nn2+(m+4)*j+2)
            print(track_name, i, j, 'k')
            track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*j+2, i*nn2+(m+4)*j+3)
            print(track_name, i, j, 'k')
            for k in range(m):
                track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*j+3+k,
                                                  i*nn2+(m+4)*j+4+k)
                print(track_name, i, j, k)
            track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*(j+1)-1,
                                              i*nn2+(m+4)*(j+1))
            print(track_name, i, j, 'k')
            track_name = 'track_%02d_%02d' % (i*nn2+(m+4)*(j+1),
                                              i*nn2+(m+4)*(j+1)+1)
            print(track_name, i, j, 'k')


def gen_line_averange(totle_length: float, number_stations: int):
    '''
example of calling:
totle_length = 1800.
number_stations = 4
sns, trs, jcts, env, stations = gen_line_averange_ver0(totle_length,
                                                       number_stations)
    '''
    # n stations
    # 2*n-2 plateforms
    #
