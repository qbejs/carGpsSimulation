import random


class OBDDevice:
    def __init__(self):
        self.speed = random.SystemRandom().uniform(40, 60)
        self.throttle_position = random.SystemRandom().uniform(40, 90)
