from core.model.source.entl_source import EntlSource



class FTPSource(EntlSource):
    UseParentforORM = True
    def __init__(self):
        self.ftp_host = None
        self.ftp_username = None
        self.ftp_password = None
        self.ftp_location = None


