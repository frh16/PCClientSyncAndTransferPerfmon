from enum import Enum

class Priority(Enum):
    NONE = 0
    BVT = 1
    HIGHT = 2
    MID = 3
    LOW = 4

class SyncType(Enum):
    NONE = 0
    DOUBLE = 1
    UPLOAD_SYNC = 2
    DOWNLOAD_SYNC = 3

