from core.model.base import Base

class EntlType(object):
    EMAIL = 'EMAIL'
    FTP = 'FTP'

class EntlSource(Base):
    def __init__(self):
        self.entl_type = None
        self.source_path = None



