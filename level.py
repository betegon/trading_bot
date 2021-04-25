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

        # TODO Round up level (maybe it should be done outside here, or not).maybe it could be done in a Chart class. A chart contains levels.
        # TODO create timeframe attribute --> HTF, MTF or LTF (Enum, as LevelType)
        # TODO create a an attribute to know how many times the level have been touched.
        # TODO set importancy of a level. Think how to know that importance (touched times, space after re-touch after broking, etc.)
        # TODO Convert from resistance to support and viceversa when broken, etc.
