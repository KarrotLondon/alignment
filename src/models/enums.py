from enum import Enum

class Frequency(Enum):
    DAILY = 1
    BIWEEKLY = 3
    WEEKLY = 7
    FORTNIGHTLY = 14
    MONTHLY = 30
    QUATERLY = 120
    ANUALLY = 365
    
class Enjoyment(Enum):
    HARD_LIMIT = 0
    SOFT_LIMIT = 1
    IF_I_MUST = 2
    IMPARTIAL = 4
    SURE_ITS_FUN = 8
    LIKE_IF = 16
    LOVE_IT = 32
    FUCKING_CANT_LIVE_WITHOUT_IT = 64
    
class Experience(Enum):
    NONE = 0
    ONCE = 1
    BEGINNER = 2
    COMPETENT = 3
    EXPERT = 5