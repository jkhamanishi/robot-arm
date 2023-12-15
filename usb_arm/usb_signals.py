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
    __class_getitem__ = classmethod(getattr)  # Enable subscription
    STOP = BitPattern(0, 0, 0)
    GRIPPERS_CLOSE = BitPattern(0x01, 0, 0)
    GRIPPERS_OPEN = BitPattern(0x02, 0, 0)
    WRIST_UP = BitPattern(0x4, 0, 0)
    WRIST_DOWN = BitPattern(0x8, 0, 0)
    ELBOW_UP = BitPattern(0x10, 0, 0)
    ELBOW_DOWN = BitPattern(0x20, 0, 0)
    SHOULDER_UP = BitPattern(0x40, 0, 0)
    SHOULDER_DOWN = BitPattern(0x80, 0, 0)
    BASE_CW = BitPattern(0, 0x01, 0)
    BASE_CCW = BitPattern(0, 0x02, 0)
    LED_ON = BitPattern(0, 0, 1)
    LED_OFF = BitPattern(0, 0, 0)
