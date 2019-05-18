from core.model.base import Base


class Role(Base):
    def __init__(self):
        self.role_name = None
        self.role_description = None
        self.system_id = None


