

class MoveGroup:
    """
    Moves multiple items simultaneously
    """
    def __init__(self, moves):
        self.moves = moves

    @property
    def finished(self):
        for m in self.moves:
            if not m.finished:
                return False
        return True

    def move(self):
        for m in self.moves:
            m.move()

    def draw(self):
        for m in self.moves:
            m.draw()

    def __repr__(self):
        return "<MoveGroup with {} moves, finished: {}>".format(len(self.moves), self.finished)
