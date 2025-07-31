from DefClass.def_error import FonctionError
from DefClass.def_line import Line


class Balise:
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.time_at_balise = []
        self.train_at_balise = []
        self.arriving_train = None
        self.x0_train = 0.
        self.x1_train = 0.
        self.info = False

    def pass_on_balise(self, train_name, time):
        self.time_at_balise.append(time)
        self.train_at_balise.append(train_name)
        self.arriving_train = None

    def add_arriving_train(self, train):
        if train.line != self.position.line:
            # the added train is not yet on the line
            self.x0_train = 0.
            self.x1_train = 0.
        else:
            self.x0_train = train.head.abs_position_line
            self.x1_train = train.head.abs_position_line
        self.arriving_train = train

    def find_arriving_train(self):
        track_temps = self.position.track
        if track_temps.list_trains_track:
            val = 0.
            for ele in track_temps.list_trains_track:
                if ele.head.track != self.position.track:
                    self.arriving_train = None
                    return None
                elif ele.head.abs_position_line < \
                        self.position.abs_position_line:
                    if ele.head.abs_position_track > val:
                        val = ele.head.abs_position_track
                        self.arriving_train = ele
                    return ele
        while not track_temps.list_trains_track:
            if track_temps.track_pre is None:
                break
            val = 0.
            track_temps = track_temps.track_pre
            for ele in track_temps.list_trains_track:
                if ele.head.abs_position_line < \
                   self.position.abs_position_line:
                    if ele.head.abs_position_track > val:
                        val = ele.head.abs_position_track
                        self.arriving_train = ele
                    return ele
        # to be completed
        return None

    def update_balise(self, time):
        if self.arriving_train is None:
            self.find_arriving_train()
        # the result of self.find_arriving_train() may keep the state None
        # of the self.arriving_train, so this conditionnal statement can -NOT-
        # be replaced by a ELSE statement
        if self.arriving_train is not None:
            if self.arriving_train.line == self.position.line:
                # the added train is not yet on the line
                self.x0_train = self.x1_train
                self.x1_train = self.arriving_train.head.abs_position_line
            else:
                self.x0_train = 0.
                self.x1_train = 0.
        self.check_train_balise(time)
        if self.info:
            self.pass_on_balise(self.arriving_train.name, time)

    def check_train_balise(self, time):
        if self.arriving_train is None:
            self.info = False
            return False
        if self.arriving_train.line != self.position.line:
            self.info = False
            return False
        if self.x1_train < self.position.abs_position_line:
            self.info = False
            return False
        elif self.x0_train <= self.position.abs_position_line:
            # consider if a preciser time is needed to calculate
            # with the passing speed and the two position values
            self.info = True
            return True
        self.info = False
        return False

    def __str__(self):
        val = 'Balise %s at %s' % (self.name, str(self.position))
        return val


class Environment:
    # definition of class Environment
    def __init__(self, name, tracks, nodes, equipements):
        self.name = name
        self.tracks = tracks
        self.nodes = nodes
        self.equipements = equipements
        self.nb_lines = 0
        self.lines = []
        self.creat_lines()
        self.trains = self.find_trains()

    def creat_lines(self):
        if not self.tracks:
            # to check if the list of tracks is empty
            raise FonctionError('in class <Environment> fct|creat_lines|, the \
list of tracks must not be empty')
        for tr in self.tracks:
            if tr.line is None:
                line_name = 'line' + str(self.nb_lines + 1)
                self.lines.append(Line(line_name, tr))
                self.nb_lines += 1

    def update_env(self):
        # great possibility to improve efficiency
        # update of the lines
        for i in range(self.nb_lines):
            del self.lines[self.nb_lines - i - 1]
        for tr in self.tracks:
            tr.line = None
        self.nb_lines = 0
        self.lines = []
        # for tr in self.tracks:
        #     tr.line = None
        self.creat_lines()
        # update of the equipements
        for ele in self.equipements:
            ele.position.update_position_line()
        # update of the signals
        # to be completed

    def set_trains(self, trains):
        return trains

    def find_trains(self):
        # to be completed
        return []

    def print_env(self):
        print('**Environment:', self.name, end='.\n')
        for li in self.lines:
            li.print_line()

    def __str__(self):
        val = '**Environment: ' + self.name + '.\n'
        for li in self.lines:
            val += str(li)
        return val + '********************************************************'
