class BitPattern(object):
    """A bit pattern to send to a robot arm"""
    __slots__ = ['arm', 'base', 'led']

    def __init__(self, arm, base, led):
        self.arm = arm
        self.base = base
        self.led = led

    def __iter__(self):
        return iter([self.arm, self.base, self.led])

    def __getitem__(self, item):
        return [self.arm, self.base, self.led][item]

    def __or__(self, other):
        return BitPattern(self.arm | other.arm,
                          self.base | other.base,
                          self.led | other.led)

    def __eq__(self, other):
        return self.arm == other.arm and self.base == other.base and self.led == other.led

    def __repr__(self):
        return "<BitPattern arm:0x%02x base:%s led:%s>" % (self.arm, self.base, self.led)

    def __str__(self):
        return self.__repr__()


class MESSAGE:

    STOP = BitPattern(0, 0, 0)

    class GRIPPERS:
        CLOSE = BitPattern(0x01, 0, 0)
        OPEN = BitPattern(0x02, 0, 0)

    class WRIST:
        UP = BitPattern(0x4, 0, 0)
        DOWN = BitPattern(0x8, 0, 0)

    class ELBOW:
        UP = BitPattern(0x10, 0, 0)
        DOWN = BitPattern(0x20, 0, 0)

    class SHOULDER:
        UP = BitPattern(0x40, 0, 0)
        DOWN = BitPattern(0x80, 0, 0)

    class BASE:
        CW = BitPattern(0, 0x01, 0)
        CCW = BitPattern(0, 0x02, 0)

    class LED:
        ON = BitPattern(0, 0, 1)
        OFF = BitPattern(0, 0, 0)
