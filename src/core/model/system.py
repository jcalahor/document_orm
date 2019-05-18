from core.model.base import Base


class System(Base):
    def __init__(self):
        self.system_name = None
        self.system_description = None
        self.contacts = []



