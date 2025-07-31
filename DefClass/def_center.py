from def_error import FonctionError


class Center:
    def __init__(self, line, dummies):
        self.line = line
        self.dummies = dummies

    def center_run(self, trains, dt):
        for du in self.dummies:
            du.train.head.distance += du.train.speed * dt * du.train.direction
