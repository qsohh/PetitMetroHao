# import matplotlib.pyplot as plt

try:
    from def_error import FonctionError
except ModuleNotFoundError:
    from DefClass.def_error import FonctionError


class Node:
    def __init__(self, name):
        self.name = name
        self.signal = False
        self.list_tracks_node = []
        self.control_by_track = True

    def signal_pass(self):
        self.signal = True

    def signal_stop(self):
        self.signal = False

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False
        if self.name == other.name:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Node):
            return True
        if self.name == other.name:
            return False
        return True


def signals2pass(list_nodes):
    for ele in list_nodes:
        if not isinstance(ele, Node):
            raise ValueError('in fct|signals2pass|, at least one of the \
elements in the list is not of type class <Node>')
        ele.signal_pass()


def signals2stop(list_nodes):
    for ele in list_nodes:
        if not isinstance(ele, Node):
            raise ValueError('in fct|signals2stop|, at least one of the \
elements in the list is not of type class <Node>')
        ele.signal_stop()


class Track:
    # definition of class Track to present a piece of track
    def __init__(self, name, length, node_origin, node_end, limit_speed=16.67):
        if node_origin == node_end:
            raise FonctionError('in class <Track> definition, origin node and \
endding node can not be the same')
        self.track_pre = None
        self.track_next = None
        self.line = None
        self.name = name
        self.tracklength = length
        self.limit_speed = limit_speed
        self.node_origin = node_origin
        # check if this track is already in the list of tracks of the node
        # if not, add it
        if self not in node_origin.list_tracks_node:
            node_origin.list_tracks_node.append(self)
        if self not in node_end.list_tracks_node:
            node_end.list_tracks_node.append(self)
        self.node_end = node_end
        self.list_trains_track = []
        self.abs_direction = [node_origin, node_end]
        self.is_platform = False

    def switch_direction(self):
        # to be modified
        node_temps = self.node_origin
        self.node_origin = self.node_end
        self.node_end = node_temps
        self.update_track()
        if self.line:
            self.line.first = self.line.node_end_line.list_tracks_node[0]
            track_temps = self.line.first
            if self.line.first != self:
                new_origin = track_temps.node_end
                track_temps.node_end = track_temps.node_origin
                track_temps.node_origin = new_origin
                track_temps.update_track()
            while track_temps.track_next is not None:
                track_temps = track_temps.track_next
                if track_temps == self:
                    continue
                new_origin = track_temps.node_end
                track_temps.node_end = track_temps.node_origin
                track_temps.node_origin = new_origin
                track_temps.update_track()
            self.line.update_line()

    def set_direction_to(self, direction, flag=True):
        # flag=True means this fct is called directely
        # flag=False means this fct is called inside itself
        self.node_end = direction
        copy = self.abs_direction[:]
        if direction in self.abs_direction:
            copy.remove(self.node_end)
            self.node_origin = copy[0]
        else:
            lt = direction.list_tracks_node[:]
            lt.remove(self)
            target_track = lt[0]
            for ele in copy:
                if target_track not in ele.list_tracks_node:
                    self.node_origin = ele
        # try:
        #     self.node_origin = copy[0]
        # except UnboundLocalError:
        #     print(self.name)
        #     print(direction.name)
        #     print(self.node_end.name)
        #     for ele in self.abs_direction:
        #         print(ele.name)
        #     raise FonctionError
        self.update_track()
        if self.line and flag:
            temp_ahead = self
            temp_back = self
            while temp_ahead.track_next is not None:
                temp_ahead.track_next.set_direction_from(temp_ahead.node_end,
                                                         False)
                temp_ahead = temp_ahead.track_next
            while temp_back.track_pre is not None:
                temp_back.track_pre.set_direction_to(temp_back.node_origin,
                                                     False)
                temp_back = temp_back.track_pre

    def set_direction_from(self, direction, flag=True):
        # flag=True means this fct is called directely
        # flag=False means this fct is called inside itself
        self.node_origin = direction
        if direction in self.abs_direction:
            copy = self.abs_direction[:]
            copy.remove(self.node_origin)
        self.node_end = copy[0]
        self.update_track()
        if self.line and flag:
            temp_ahead = self
            temp_back = self
            while temp_ahead.track_next is not None:
                temp_ahead.track_next.set_direction_from(temp_ahead.node_end,
                                                         False)
                temp_ahead = temp_ahead.track_next
            while temp_back.track_pre is not None:
                temp_back.track_pre.set_direction_to(temp_back.node_origin,
                                                     False)
                temp_back = temp_back.track_pre

    def update_track(self):
        if len(self.node_origin.list_tracks_node) == 1:
            self.track_pre = None
        elif not self.node_origin.signal:
            self.track_pre = None
        else:
            list_temps = self.node_origin.list_tracks_node[:]
            list_temps.pop(list_temps.index(self))
            self.track_pre = list_temps[0]
        if len(self.node_end.list_tracks_node) == 1:
            self.track_next = None
        elif not self.node_end.signal:
            self.track_next = None
        else:
            list_temps = self.node_end.list_tracks_node[:]
            list_temps.pop(list_temps.index(self))
            self.track_next = list_temps[0]
        if self.list_trains_track:  # and self.node_origin.control_by_track:
            self.node_origin.signal_stop()
        elif self.node_origin.control_by_track:
            self.node_origin.signal_pass()
        else:
            pass

    def print_track(self):
        print('| Track:', self.name, end='. ')
        print('From',
              self.node_origin.name, 'to', self.node_end.name, end='. ')
        if self.track_pre is None:
            print('Pre is None; ', end='')
        else:
            print('Pre', self.track_pre.name, end='; ')
        if self.track_next is None:
            print('next is None')
        else:
            print('next', self.track_next.name)

    def __str__(self):
        val = '| Track ' + self.name + '. '
        val += 'length ' + str(self.tracklength) + '. '
        val += 'From ' + self.node_origin.name
        val += ' to ' + self.node_end.name + '. '
        if self.track_pre is None:
            val += 'Pre is None; '
        else:
            val += 'Pre ' + self.track_pre.name + '; '
        if self.track_next is None:
            val += 'next is None'
        else:
            val += 'next ' + self.track_next.name
        return val + '.\n'

    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        if self.name == other.name:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Track):
            return True
        if self.name == other.name:
            return False
        return True


class Line:
    # definition of class Track to present a line of tracks
    def __init__(self, name, firsttrack):
        # the first_track's nodes and direction should be well defined
        self.name = name
        self.first = firsttrack
        firsttrack.line = self
        self.list_tracks = [firsttrack]
        self.node_origin_line = firsttrack.node_origin
        self.node_end_line = firsttrack.node_end
        self.tracklength_line = 0.
        self.update_line()
        self.iscircle = self.check_circle()
        # the set of trains on the line to be completed
        self.list_trains_line = []
        # the set of trains on the line to be completed
        list_temps1, list_temps2 = self.set_limit_speed_line()
        self.coor_limit_speed = list_temps1
        self.limit_speed_line = list_temps2
        self.list_balises = []

    def check_first(self):
        self.first.update_track()
        if self.first.track_pre is None:
            return True
        elif self.check_circle():
            return True
        return False

    def find_real_first(self):
        if self.check_circle():
            self.node_origin_line = self.first.node_origin
            self.first.line = self
            return self.first
        while not self.check_first():
            self.first = self.first.track_pre
            self.first.line = self
            self.first.update_track()
            self.list_tracks = [self.first]
            self.node_origin_line = self.first.node_origin
        return self.first

    def check_circle(self):
        track_temps = self.first
        self.first.update_track()
        while track_temps.track_next is not None:
            if track_temps.track_next.node_origin != track_temps.node_end:
                track_temps.track_next.switch_direction()
            track_temps = track_temps.track_next
            if track_temps.track_next == self.first:
                return True
        return False

    def update_line(self):
        # to update the tracks in the list_tracks and the two nodes of the line
        # the first_track's nodes and direction of the line should be
        # well defined
        track_temps = self.find_real_first()
        self.node_origin_line = track_temps.node_origin
        self.node_end_line = track_temps.node_end
        self.list_tracks = []
        self.list_tracks.append(track_temps)
        self.tracklength_line = track_temps.tracklength
        while track_temps.track_next is not None:
            if track_temps.track_next.node_origin != track_temps.node_end:
                track_temps.track_next.switch_direction()
            if track_temps not in self.list_tracks:
                track_temps.update_track()
                track_temps.line = self
                self.tracklength_line += track_temps.tracklength
                self.list_tracks.append(track_temps)
            track_temps = track_temps.track_next
            self.node_end_line = track_temps.node_end
            track_temps.update_track()
            track_temps.line = self
            self.tracklength_line += track_temps.tracklength
            self.list_tracks.append(track_temps)
            if track_temps.track_next == self.first:
                track_temps.update_track()
                track_temps.line = self
                self.tracklength_line += track_temps.tracklength
                self.list_tracks.append(track_temps)
                self.node_end_line = track_temps.node_end
                break
        list_temps1, list_temps2 = self.set_limit_speed_line()
        self.coor_limit_speed = list_temps1
        self.limit_speed_line = list_temps2

    def set_limit_speed_line(self):
        # update the line before call this method
        coor_limit_speed = []
        limit_speed_line = []
        val = 0.
        coor_limit_speed.append(0.)
        limit_speed_line.append(self.first.limit_speed)
        for ele in self.list_tracks:
            if limit_speed_line[-1] != ele.limit_speed:
                coor_limit_speed.append(val)
                limit_speed_line.append(ele.limit_speed)
            val += ele.tracklength
        coor_limit_speed.append(self.tracklength_line)
        limit_speed_line.append(0.)
        # to be completed
        return coor_limit_speed, limit_speed_line

    def position_on_line(self, position):
        val = 0
        track_temps = position.track
        for ele in track_temps.line.list_tracks:
            if ele == track_temps:
                if track_temps.abs_direction[1] == track_temps.node_end:
                    val += position.abs_position_track
                else:
                    val += (track_temps.length - position.abs_position_track)
                break
            else:
                val += ele.length
        return val

    def coord_track2line(self, position):
        val = 0
        track_temps = position.track
        for ele in track_temps.line.list_tracks:
            if ele == track_temps:
                if track_temps.abs_direction[1] == track_temps.node_end:
                    val += position.abs_position_track
                else:
                    val += (track_temps.tracklength -
                            position.abs_position_track)
                break
            else:
                val += ele.tracklength
        return val

    def show_limit_speed_info(self):
        X = self.coor_limit_speed
        Y = self.limit_speed_line
        length_data = len(X)
        for i in range(length_data):
            if X[length_data-i-1]:
                X.insert(length_data-i-1, X[length_data-i-1])
            if Y[length_data-i-1]:
                Y.insert(length_data-i-1, Y[length_data-i-1])
        # plt.plot(X, Y, 'r')
        # plt.show()
        return X, Y

    def print_line(self):
        print('-Line:', self.name, end='. ')
        print('From', self.node_origin_line.name,
              'to', self.node_end_line.name, end='. ')
        print('Total length', self.tracklength_line, 'm.')
        for ele in self.list_tracks:
            ele.print_track()

    def __eq__(self, other):
        if not isinstance(other, Line):
            return False
        if self.name == other.name:
            return True
        return False

    def __ne__(self, other):
        if not isinstance(other, Line):
            return True
        if self.name == other.name:
            return False
        return True

    def __str__(self):
        val = '-Line: {%s}. ' % self.name
        val += 'From (%s)' % self.node_origin_line.name
        val += ' to (%s).' % self.node_end_line.name
        val += 'Total length ' + str(self.tracklength_line) + ' m.\n'
        for ele in self.list_tracks:
            val += str(ele)
        return val


class Junction:
    def __init__(self, name, node1, node2):
        self.name = name
        self.node1 = node1
        self.node2 = node2
        self.nodes = [node1, node2]
        list_tr1 = node1.list_tracks_node
        list_tr2 = node2.list_tracks_node
        # whether need to check the length of these two lists or not
        commun_track = []
        for ele in node1.list_tracks_node:
            if ele in node2.list_tracks_node:
                commun_track.append(ele)
        # possibility to improve the functionnality
        if len(commun_track) != 1:
            raise ValueError('in class <Junction(Joint)> definition, the two \
nodes have no commun track or more than one commun track')
        self.track_main = commun_track.pop()
        list_tr1.pop(list_tr1.index(self.track_main))
        self.brench_track_n1 = list_tr1[0]
        list_tr2.pop(list_tr2.index(self.track_main))
        self.brench_track_n2 = list_tr2[0]

    def switch(self, target_node=None):
        if target_node:
            if target_node not in self.nodes:
                raise ValueError('in class <Junction(Joint)> fct |switch|, \
the target node is not one of the junctions <Node>s')
            self.switch_to(target_node)
        elif self.node1.signal is False and self.node2.signal is False:
            raise ValueError('in class <Junction(Joint)> fct |switch|, \
both the two <Node>s\' signals are False')
        elif self.node1.signal:
            self.switch_to(self.node2)
        else:
            self.switch_to(self.node1)

    def switch_to(self, target_node):
        # each time calling <Junction>.|switch_to|, considerate if the change
        # of direction of the train is also needed
        if target_node not in self.nodes:
            raise ValueError('in class <Junction(Joint)> fct |switch_to|, \
the target node is not one of the junctions <Node>s')
        signals2stop(self.nodes)
        target_node.signal_pass()
        if target_node not in self.track_main.abs_direction:
            lt = self.track_main.abs_direction
            if self.node1 == target_node:
                lt[lt.index(self.node2)] = self.node1
            else:
                lt[lt.index(self.node1)] = self.node2
        self.track_main.set_direction_to(target_node)
        # if self.track_main.node_end != target_node:
        #     self.track_main.switch_direction()
        #     self.track_main.track_pre = self.track_main.track_next
        if self.node1 == target_node:
            self.track_main.track_next = self.brench_track_n1
        else:
            self.track_main.track_next = self.brench_track_n2
        self.track_main.node_end = target_node
        if len(target_node.list_tracks_node) == 1:
            target_node.list_tracks_node.append(self.track_main)

    def switch_from(self, target_node):
        if target_node not in self.nodes:
            raise ValueError('in class <Junction(Joint)> fct |switch_from|, \
the target node is not one of the junctions <Node>s')
        signals2stop(self.nodes)
        target_node.signal_pass()
        if target_node not in self.track_main.abs_direction:
            lt = self.track_main.abs_direction
            if self.node1 == target_node:
                lt[lt.index(self.node2)] = self.node1
            else:
                lt[lt.index(self.node1)] = self.node2
        self.track_main.set_direction_from(target_node)
        # if self.track_main.node_origin != target_node:
        # if self.track_main.node_origin not in self.nodes:
        #     self.track_main.switch_direction()
        if self.node1 == target_node:
            self.track_main.track_pre = self.brench_track_n1
        else:
            self.track_main.track_pre = self.brench_track_n2
        self.track_main.node_origin = target_node
        if len(target_node.list_tracks_node) == 1:
            target_node.list_tracks_node.append(self.track_main)


class Crossing():
    # not used yet
    def __init__(self, name, track1, track2):
        self.name = name
        self.track1 = track1
        self.track2 = track2
