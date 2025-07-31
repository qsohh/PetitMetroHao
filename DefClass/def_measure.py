# from def_error import FonctionError


class Measure:
    def __init__(self, Train):
        self.train = Train
        self.name = Train.name + '_measure'
        self.position = Train.head  # + random_variable
        self.speed = Train.speed  # + random_variable

    def remeasure(self):
        # update the train before remeasure it
        self.position = self.train.head  # + random_variable
        self.speed = self.train.speed  # + random_variable
        # self.train.tail = self.train.find_tail()
