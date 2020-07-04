class Bubble:
    def __init__(self):
        self.spawn()

    def spawn(self):
        self.size = 16

    def move(self, delay):
        pass


class Player(Bubble):

    def __init__(self):
        super().__init__()

    def deviate_up(self, delay):
        self.deviate(0, delay)

    def deviate_down(self, delay):
        self.deviate(0, -delay)

    def deviate_right(self, delay):
        self.deviate(delay, 0)

    def deviate_left(self, delay):
        self.deviate(-delay, 0)

    def deviate(self, x, y):
        pass
