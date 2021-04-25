from enum import Enum

class LevelType(Enum):
    SUPPORT = 'SUPPORT'
    RESISTANCE = 'RESISTANCE'

class Level():
    def __init__(self, type: LevelType, touched: bool = None, 
                 broken: bool = None, traded: bool = None):
        if not isinstance(type, LevelType):
            raise ValueError(
                'You tried to set Level.type = {}, '
                'but It should be one of these: {}'.format(type, [e.value for e in LevelType]))
        self.type = type
        self.touched = touched or False
        self.broken = broken or False
        self.traded = traded or False
        # TODO create a an attribute to know how many times the level have been touched.
        # TODO set importancy of a level.
