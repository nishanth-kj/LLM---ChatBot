import enum

class Status(enum.Enum):
    ACTIVE = ("Active", 1)
    INACTIVE = ("Inactive", 2)
    PENDING = ("Pending", 3)
    APPROVED = ("Approved", 4)
    REJECTED = ("Rejected", 5)
    DELETED = ("Deleted", 7)
    ERROR = ("Error", 6)

    def __init__(self, label, code):
        self.label = label
        self.code = code