from DefClass.def_error import FonctionError
from DefClass.def_train import Position


class Dummy:
    def __init__(self, Measure):
        self.measure = Measure
        self.train = Measure.train
        self.train.dummy = self
        self.name = Measure.train.name + '_dummy'
        self.line = self.train.line
        self.position = Measure.position
        self.measured_tail = self.find_dummy_tail()
        # another find tail is needed
        self.speed = Measure.speed
        self.stopping_time = 0.
        # self.state_set('STOP')
        self.state = 'STOP'
        self.at_station = False
        # possible states: ['RUN' 'BRAKE' 'STATION' 'STOP_LINE']
        self.dis_before_stop = self.dis_before_stop_cal()
        # self.target_speed = self.target_speed_cal()
        self.dis_2_change, self.next_speed = self.dis_2_change_cal()
        self.D2V = []
        self.NVC = []

    def state_set(self, state):
        self.state = state

    def command(self, dt):
        #################################################
        # this is the most important fct of the project #
        #################################################
        self.update_dummy()
        self.train.state[self.state](dt)
        self.dis_2_change, self.next_speed = self.dis_2_change_cal()
        if (self.state == 'RUN' or self.state == 'IDLE') and \
           self.dis_2_end_cal() - self.dis_before_stop_cal() <= 10.:
            # this behavior to be improuved
            self.state_set('BRAKE')
            self.target_speed_set(0.)
            self.record_dummy()
            return None
        if self.state == 'BRAKE' and self.speed == 0.:
            self.state_set('STOP')
            self.record_dummy()
            return None
        if self.state == 'STOP':
            if self.at_station:
                if self.train.demande_leaving() and self.dis_2_end_cal() > 10.:
                    self.state_set('RUN')
            else:
                if self.dis_2_end_cal() > 10.:
                    self.state_set('RUN')
        if self.dis_2_change <= 5.:
            self.target_speed_set(self.next_speed)
        elif self.dis_2_end_cal() - self.dis_before_stop_cal() > 0:
            # to be modified after the fct <Train>.|find_tracks| is finished
            # then will set the min of the limit speeds of all tracks in the
            # list of tracks
            limit_speed_min = []
            for ele in self.train.tracks:
                limit_speed_min.append(ele.limit_speed)
            self.target_speed_set(min(limit_speed_min))
        self.record_dummy()
        return None
#         print('FctWarning: in class <Dummy> %s.fct|command(dt)|, when a \
# train is about to slow down, there will be a moment when his target speed \
# returns to the previous target speed which is needed to be modified')

    def update_dummy(self):
        # self.train.update_train()
        self.measure.remeasure()
        self.line = self.train.line
        self.position = self.measure.position
        self.speed = self.measure.speed
        self.stop_time = 0.
        self.dis_before_stop = self.dis_before_stop_cal()
        self.dis_2_change, self.next_speed = self.dis_2_change_cal()
        self.measured_tail = self.find_dummy_tail()

    def dis_2_end_cal(self):
        # to be completed
        dis = self.train.line.tracklength_line - \
              self.position.abs_position_line
        return dis

    def dis_before_stop_cal(self):
        dis = (self.speed**2) / abs(2*self.train.acceleration_braking)
        return dis

    def target_speed_cal(self):
        print('FctWarning: in class <Dummy> %s.fct|target_speed_cal|, method \
to be completed' % (self.name))
        # to be completed
        return None

    def target_speed_set(self, target_speed):
        self.target_speed = target_speed
        self.train.target_speed = target_speed

    def dis_2_change_cal(self):
        # to be completed
        dis = self.dis_2_end_cal() - self.dis_before_stop_cal() + 5
        next_speed = 0.
        coor = self.line.coor_limit_speed
        speeds = self.line.limit_speed_line
        for i in range(len(coor)):
            if coor[i] < self.position.abs_position_line:
                continue
            if self.speed > speeds[i]:
                # think over which way could be more accurate:
                # a**2-b**2 or (a+b)*(a-b)
                val = (self.speed - speeds[i]) * (self.speed + speeds[i]) / \
                      (2 * self.train.acceleration_negative)
                # a gap of distance is waiting to be added
                val += coor[i] - self.position.abs_position_line
                if val < dis:
                    dis = val
                    next_speed = speeds[i]
        return dis, next_speed

    def find_dummy_tail(self):
        # the direction of tracks and the line must be well defined before
        # calling this find_tail method
        # in fact this method should be introduced in the class <Position>
        # so this is waiting to be modified
        track_temps = self.position.track
        val = self.position.coord_on_track() - self.train.length
        if val >= 0.:
            if self.train.direction == self.position.track.abs_direction[1]:
                return Position(track_temps, val)
            else:
                return Position(track_temps, track_temps.tracklength - val)
        else:
            while val < 0.:
                lt = track_temps.node_origin.list_tracks_node[:]
                if len(lt) <= 1:
                    print(self.name)
                    print(len(lt))
                    raise FonctionError('in class <Dummy> fct|find_dummy_tail|\
, can not find tail on current line')
                lt.remove(track_temps)
                track_temps = lt[0]
                val += track_temps.tracklength
            if self.train.direction == self.position.track.abs_direction[1]:
                return Position(track_temps, val)
            else:
                return Position(track_temps, track_temps.tracklength - val)
        raise FonctionError('in class <Train> fct|find_tail|, can not find \
tail on current line')
        return None

    def record_dummy(self):
        self.D2V.append(self.dis_2_change)
        self.NVC.append(self.next_speed)

    def print_dummy(self):
        print('-----------------------------------')
        print('Dummy: ', self.name)
        print('Head position:', str(self.position))
        print('Tail position:', str(self.train.tail))
        # another find tail is needed
        print('Current speed: ', self.speed)
        print('On the track(s): ')
        for tr in self.train.tracks:
            print(tr.name, ';', end='')
        print('\nHead direction: ', self.train.direction.name)
        print('-----------------------------------')
