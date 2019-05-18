from core.model.user import User

class ExternalUser(User):
    def __init__(self):
        self.company_name = None
        self.mailing_address = None


