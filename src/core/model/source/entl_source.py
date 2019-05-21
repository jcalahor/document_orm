from core.model.base import Base

class EntlType(object):
    EMAIL = 'EmailSource'
    FTP = 'FTPSource'

class EntlSource(Base):
    def __init__(self):
        self.entl_type = None
        self.source_path = None



