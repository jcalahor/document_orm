from core.model.base import Base

class User(Base):
    def __init__(self):
        self.first_name = None
        self.last_name = None
        self.email = None



