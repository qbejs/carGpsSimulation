import random


class OBDDevice:
    def __init__(self):
        self.speed = random.randint(40, 60)
        self.throttle_position = random.randint(25, 90)
