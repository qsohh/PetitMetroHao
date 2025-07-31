from DefClass.def_error import FonctionError, StateError


class Position:
    def __init__(self, track, position):
        self.track = track
        self.line = self.track.line
        self.abs_position_track = position
        if self.track.line is None:
            raise FonctionError('in class <Position> definition, the line \
must be set before the definition of Position \n(initialize the environment \
first and then creat the position)')
        self.abs_position_line = self.track.line.coord_track2line(self)

    def coord_line2track(self):
        # the coordinate of the origin of current track
        val = 0
        for ele in self.line.list_tracks:
            # check if the point is in the current track (ele)
            if val + ele.tracklength > self.abs_position_line:
                new_position_track = self.abs_position_line - val
                # check the abs direction of the current track
                if ele.node_end != ele.abs_direction[1]:
                    new_position_track = ele.tracklength - new_position_track
                self.track = ele
                self.abs_position_track = new_position_track
                return self
            val += ele.tracklength
        raise FonctionError('in class <Position> fct|coord_line2track|, can \
not find position on current line')

    def coord_on_track(self):
        # the distance from the node_origin to the <Position> self
        if self.track.node_origin in self.track.abs_direction:
            if self.track.node_origin == self.track.abs_direction[0]:
                return self.abs_position_track
            else:
                return self.track.tracklength - self.abs_position_track
        elif self.track.node_end in self.track.abs_direction:
            if self.track.node_end == self.track.abs_direction[1]:
                return self.abs_position_track
            else:
                return self.track.tracklength - self.abs_position_track
        else:
            raise FonctionError('in class <Position>.fct|coord_on_track|, \
most strange error')

    def update_position_line(self):
        self.line = self.track.line
        self.abs_position_line = self.track.line.coord_track2line(self)

    def copy(self):
        return Position(self.track, self.abs_position_track)

    def __str__(self):
        val = '[%-9s] %-9.3f m. ' % (self.track.name, self.abs_position_track)
        val += '{%-9s} %-9.3f m.' % (self.track.line.name,
                                     self.abs_position_line)
        return val


class Train:
    # these constantes to be modified
    acceleration_positive = 2.  # m/s2
    acceleration_negative = -2.  # m/s2
    acc_idle = -0.5  # m/s2
    acceleration_braking = -3.  # m/s2
    urgent_brake = -4.  # m/s2
    speed_max = 40.  # m/s

    def __init__(self, name, length, position_head, direction):
        # version 0 : definition of direction : the end of the current track
        # this node of direction need to be modified by time
        self.name = name
        self.length = length
        self.head = position_head
        self.line = position_head.track.line
        self.direction = direction
        self.reset_line_direction()
        self.tail = self.find_tail()
        self.end_ahead = position_head.track.line.node_end_line
        self.speed = 0.
        self.target_speed = 0.
        self.find_tracks()
        for ele in self.tracks:
            if self not in ele.list_trains_track:
                ele.list_trains_track.append(self)
        # not need for the first fixed blocks model
        self.train_pre = None
        self.train_next = None
        # block the signal behind
        self.node_behind = self.find_node_behind()
        self.state = {'RUN': self.run,
                      'IDLE': self.idle,
                      'BRAKE': self.brake,
                      'STOP': self.stop}
        self.stopping_time = 0.
        self.dummy = None
        # need a variable to stock the total distance of the previous lines
        self.distance_covered = 0.  # the distance of the previous lines
        self.DD = []
        self.VV = []
        self.TV = []
        self.PP = []

    def reset_line_direction(self):
        if self.head.track not in self.direction.list_tracks_node:
            raise FonctionError('in class <Train> fct|reset_line_direction|, \
direction node not found in the current track')
        # self.line.update_line()
        if self.direction != self.head.track.node_end:
            new_first = self.line.node_end_line.list_tracks_node[0]
            self.line.first = new_first
            new_first.switch_direction()
        self.line.update_line()

    def position_repere_line(self):
        val = 0
        for ele in self.line.list_tracks:
            if ele == self.head.track:
                if self.head.track.abs_direction[1] == \
                   self.head.track.node_end:
                    val += self.head.abs_position_track
                else:
                    val += (self.head.track.tracklength -
                            self.head.abs_position_track)
                break
            else:
                val += ele.tracklength
        return val

    def find_tail(self):
        # the direction of tracks and the line must be well defined before
        # calling this find_tail method
        # in fact this method should be introduced in the class <Position>
        # so this is waiting to be modified
        track_temps = self.head.track
        val = self.head.coord_on_track() - self.length
        if val >= 0.:
            if self.direction == self.head.track.abs_direction[1]:
                return Position(track_temps, val)
            else:
                return Position(track_temps, track_temps.tracklength - val)
        else:
            while val < 0.:
                lt = track_temps.node_origin.list_tracks_node[:]
                if len(lt) <= 1:
                    print(self.name)
                    print('head', self.head)
                    print('tail', self.tail)
                    print(self.direction.name)
                    print(track_temps.node_origin.name)
                    raise FonctionError('in class <Train> fct|find_tail|, can \
not find tail on current line')
                lt.remove(track_temps)
                track_temps = lt[0]
                val += track_temps.tracklength
            if self.direction == self.head.track.abs_direction[1]:
                return Position(track_temps, val)
            else:
                return Position(track_temps, track_temps.tracklength - val)
        raise FonctionError('in class <Train> fct|find_tail|, can not find \
tail on current line, most strange FonctionError')
        return None

    def find_tail_old_version_not_valid(self):
        # def find_tail(self):
        # the direction of tracks and the line must be well defined before
        # calling this find_tail method
        # in fact this method should be introduced in the class <Position>
        # so this is waiting to be modified
        position_tail_line = self.position_repere_line() - self.length
        val = 0
        for ele in self.line.list_tracks:
            if val + ele.tracklength > position_tail_line:
                position_tail_track = position_tail_line - val
                # check the abs direction of the current track
                if ele.node_end != ele.abs_direction[1]:
                    position_tail_track = ele.tracklength - position_tail_track
                position_tail = Position(ele, position_tail_track)
                return position_tail
            # else:
            #     position_tail_line =
            #     position_tail = Position(ele, position_tail_line)
            #     return position_tail
            val += ele.tracklength
        raise FonctionError('in class <Train> fct|find_tail|, can not find \
tail on current line')
        # return position_tail

    def find_node_behind(self):
        position_tail_line = self.position_repere_line() - self.length
        val = 0
        for ele in self.line.list_tracks:
            if val + ele.tracklength > position_tail_line:
                node_found = ele.node_origin
            val += ele.tracklength
        # raise FonctionError('in class <Train> fct|find_node_behind|, can not\
# find the right node on current line')
        return node_found

    def find_tracks(self):
        # to be called after well define the head and the tail of the train
        self.tracks = []
        self.tracks.append(self.head.track)
        if self.head.track == self.tail.track:
            return self.tracks
#         if self.head.track.track_next == None:
#             raise FonctionError('in class <Train> fct|find_tracks|, the \
# train on the last track but the tail is not on the same track')
        else:
            lt = self.head.track.node_origin.list_tracks_node[:]
            if len(lt) <= 1:
                raise FonctionError('in class <Train> fct|find_tail|, error \
for the length of node_origin\'s list_tracks_node')
            lt.remove(self.head.track)
            ele_track = lt[0]
            self.tracks.append(ele_track)
            while ele_track is not self.tail.track:
                lt = ele_track.node_origin.list_tracks_node[:]
                if len(lt) <= 1:
                    raise FonctionError('in class <Train> fct|find_tail|, \
error for the length of node_origin\'s list_tracks_node')
                lt.remove(ele_track)
                ele_track = lt[0]
                self.tracks.append(ele_track)
            return self.tracks
#         print('FctWarning: in class <Train> %s.fct|find_tracks|, \
# method to be completed' %(self.name))
        raise FonctionError('in class <Train>.fct|find_tracks|, most strange \
FonctionError')

    def update_train(self):
        self.line = self.head.track.line
        # to be modified if the direction is changed
        self.direction = self.head.track.node_end
        self.reset_line_direction()
        self.head.update_position_line()
        self.tail = self.find_tail()
        self.end_ahead = self.head.track.line.node_end_line
        self.end_behind = self.find_node_behind()
        self.find_tracks()
        for ele in self.tracks:
            if self not in ele.list_trains_track:
                ele.list_trains_track.append(self)
        # not need for the first fixed blocks model
        self.train_pre = None
        self.train_next = None
        # block the signal behind
        self.node_behind = self.find_node_behind()

    def change_direction(self):
        new_head = self.tail
        self.tail = self.head
        self.head = new_head
        if self.direction == self.head.track.node_end:
            self.head.track.switch_direction()
        self.update_train()

    def run(self, dt):
        self.stopping_time = 0.
        # to be completed
        condition_keep = ((dt * self.acceleration_negative) <
                          (self.target_speed - self.speed)) and \
                         ((self.target_speed - self.speed) <
                          (dt * self.acceleration_positive))
        if condition_keep:
            self.speed = self.target_speed
        elif self.speed < self.target_speed:
            self.speed += dt * self.acceleration_positive
        else:
            self.speed += dt * self.acceleration_negative
        self.head.abs_position_line += dt * self.speed
        track_temps = self.head.track
        track_tail = self.tail.track
        self.head.coord_line2track()
        self.tail = self.find_tail()
        if track_temps != self.head.track:
            self.distance_covered += track_temps.tracklength
        if track_tail != self.tail.track:
            track_tail.list_trains_track.remove(self)
        self.record_train()

    def idle(self, dt):
        self.stopping_time = 0.
        if abs(self.speed) < abs(dt * self.acc_idle):
            self.speed = 0
        else:
            self.speed += dt * self.acc_idle
            self.head.abs_position_line += dt * self.speed
            track_temps = self.head.track
            track_tail = self.tail.track
            self.head.coord_line2track()
            self.tail = self.find_tail()
            if track_temps != self.head.track:
                self.distance_covered += track_temps.tracklength
            if track_tail != self.tail.track:
                track_tail.list_trains_track.remove(self)
        print('FctWarning: in class <Train> fct|idle|, IDLE model to be \
improved')
        self.record_train()

    def brake(self, dt):
        self.stopping_time = 0.
        # to be completed
        if abs(self.speed) < abs(dt * self.acceleration_braking):
            self.speed = 0
            self.dummy.state_set('STOP')
        else:
            self.speed += dt * self.acceleration_braking
            self.head.abs_position_line += dt * self.speed
            track_temps = self.head.track
            track_tail = self.tail.track
            self.head.coord_line2track()
            self.tail = self.find_tail()
            if track_temps != self.head.track:
                self.distance_covered += track_temps.tracklength
            if track_tail != self.tail.track:
                track_tail.list_trains_track.remove(self)
            # to change the state of dummy to 'STOP'
            # need to add the dummy to the attribute of the class <Train>
        self.record_train()

    def stop(self, dt=0.1):
        # to be completed
        self.stopping_time += dt
        if self.speed:
            raise StateError('Train %s speed not zero for state \'STOP\'' %
                             (self.name))
        self.record_train()

    def demande_leaving(self):
        if self.stopping_time >= 30.:
            return True
        elif not self.head.track.is_platform:
            return True
        else:
            return False

    def record_train(self):
        self.update_train()
        # self.DD.append(self.head.abs_position_track + self.distance_covered)
        self.DD.append(self.head.coord_on_track() + self.distance_covered)
        self.VV.append(self.speed)
        self.TV.append(self.target_speed)
        self.PP.append(self.head.copy())

    def print_train(self):
        print('===================================')
        print('Train Number: ', self.name)
        print('Head position:', str(self.head))
        print('Tail position:', str(self.tail))
        print('Current speed: ', self.speed)
        print('On the track(s): ')
        for tr in self.tracks:
            print(tr.name, ';', end='')
        print('\nHead direction: ', self.direction.name)
        print('===================================')

    def __str__(self):
        val = ''
        return val
