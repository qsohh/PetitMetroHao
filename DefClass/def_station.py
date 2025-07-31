class Station:
    def __init__(self, name, main_track, entry, exit, balise_ap, balise_en,
                 balise_nn, signal_ap):
        self.name = name
        self.main_track = main_track
        main_track.is_platform = True
        self.entry = entry
        self.entry.control_by_track = False
        self.exit = exit
        self.exit.control_by_track = False
        self.balise_ap = balise_ap
        self.balise_en = balise_en
        self.balise_nn = balise_nn
        self.signal_ap = signal_ap
        self.signal_ap.control_by_track = False
        self.state = None
        self.stopping_time = 0.
        self.passing_train = None
        self.comming_train = None
        self.transit = {'AP': self.ap,
                        'EN': self.en,
                        'ST': self.st,
                        'LV': self.lv,
                        'NN': self.nn}
        self.waiting_train = False

    def ap(self, time, dt):
        self.find_trains()
        if self.balise_ap.info:
            self.waiting_train = True
        if self.balise_en.info:
            self.state = 'EN'
            self.exit.signal_stop()
            self.signal_ap.signal_stop()

    def en(self, time, dt):
        self.find_trains()
        if self.balise_ap.info:
            self.waiting_train = True
        if self.passing_train.speed == 0.:
            self.state = 'ST'
            self.entry.signal_stop()

    def st(self, time, dt):
        self.find_trains()
        self.stopping_time += dt
        if self.balise_ap.info:
            self.waiting_train = True
        if self.stopping_time >= 22. and not \
                self.balise_nn.position.track.list_trains_track:
            self.state = 'LV'
            self.exit.signal_pass()

    def lv(self, time, dt):
        self.find_trains()
        if self.balise_ap.info:
            self.waiting_train = True
        if self.balise_nn.info:
            self.state = 'NN'
            self.passing_train = None
            self.signal_ap.signal_pass()
            self.entry.signal_pass()
            self.exit.signal_stop()

    def nn(self, time, dt):
        self.find_trains()
        if self.balise_ap.info:
            self.waiting_train = True
            # self.balise_ap.arriving_train = None
        if self.waiting_train:
            self.state = 'AP'
            self.passing_train = self.comming_train
            self.comming_train = None
            # self.comming_train = self.balise_ap.arriving_train
            self.waiting_train = False
        self.find_trains()

    def control(self, time, dt):
        # update the balises
        self.balise_ap.update_balise(time)
        self.balise_en.update_balise(time)
        self.balise_nn.update_balise(time)
        self.transit[self.state](time, dt)

    def find_trains(self):
        self.balise_ap.find_arriving_train()
        self.balise_en.find_arriving_train()
        self.balise_nn.find_arriving_train()
        if not self.comming_train:
            self.comming_train = self.balise_ap.arriving_train

    def set_passing_train(self, train, time):
        self.passing_train = train
        self.balise_ap.update_balise(time)
        self.balise_en.update_balise(time)
        self.balise_nn.update_balise(time)


class Terminus_v0:
    def __init__(self, name, main_track, entry, exit, end, balise_ap,
                 balise_en, balise_nn, signal_ap, junction):
        self.name = name
        self.main_track = main_track
        main_track.is_platform = True
        self.entry = entry
        self.entry.control_by_track = False
        self.exit = exit
        self.exit.control_by_track = False
        self.end = end
        self.end.control_by_track = False
        self.balise_ap = balise_ap
        self.balise_en = balise_en
        self.balise_nn = balise_nn
        self.signal_ap = signal_ap
        self.signal_ap.control_by_track = False
        self.junction = junction
        self.state = None
        self.stopping_time = 0.
        self.passing_train = None
        self.comming_train = None
        self.transit = {'AP': self.ap,
                        'EN': self.en,
                        'ST': self.st,
                        'LV': self.lv,
                        'NN': self.nn}
        self.waiting_train = False

    def ap(self, time, dt):
        self.stopping_time = 0.
        self.find_trains()
        if self.balise_ap.info:
            self.waiting_train = True
        if self.balise_en.info:
            self.state = 'EN'
            self.exit.signal_stop()
            self.signal_ap.signal_stop()

    def en(self, time, dt):
        self.find_trains()
        if self.balise_ap.info:
            self.waiting_train = True
        if self.passing_train.speed == 0.:
            self.state = 'ST'
            self.entry.signal_stop()

    def st(self, time, dt):
        self.find_trains()
        self.stopping_time += dt
        if self.balise_ap.info:
            self.waiting_train = True
        if self.stopping_time >= 25.:
            self.state = 'LV'
            self.junction.switch_to(self.exit)
            # self.passing_train.update_train()
            if self.passing_train.direction == self.end:
                self.passing_train.change_direction()
            self.passing_train.update_train()
            # self.exit.signal_pass()
            # change the direction !!!!!!!!

    def lv(self, time, dt):
        self.find_trains()
        if self.balise_ap.info:
            self.waiting_train = True
            if self.comming_train is None:
                print('Pb1')
        if self.balise_nn.info:
            self.state = 'NN'
            self.passing_train.at_station = False
            self.passing_train = None
            self.signal_ap.signal_pass()
            self.junction.switch_from(self.entry)
            # self.entry.signal_pass()
            # self.exit.signal_stop()

    def nn(self, time, dt):
        self.find_trains()
        if self.balise_ap.info:
            self.waiting_train = True
            # self.balise_ap.arriving_train = None
        if self.waiting_train:
            self.state = 'AP'
            self.passing_train = self.comming_train
            self.comming_train = None
            # self.comming_train = self.balise_ap.arriving_train
            self.waiting_train = False
        self.find_trains()

    def control(self, time, dt):
        # update the balises
        self.balise_ap.update_balise(time)
        self.balise_en.update_balise(time)
        self.balise_nn.update_balise(time)
        self.transit[self.state](time, dt)

    def find_trains(self):
        self.balise_ap.find_arriving_train()
        self.balise_en.find_arriving_train()
        self.balise_nn.find_arriving_train()
        if not self.comming_train:
            self.comming_train = self.balise_ap.arriving_train

    def set_passing_train(self, train, time):
        self.passing_train = train
        self.balise_ap.update_balise(time)
        self.balise_en.update_balise(time)
        self.balise_nn.update_balise(time)


class Terminus(Station):
    def __init__(self):
        pass
