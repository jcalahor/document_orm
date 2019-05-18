from core.model.source.entl_source import EntlSource



class EmailSource(EntlSource):
    UseParentforORM = True
    def __init__(self):
        self.sender_email = None
        self.subject_pattern = None

