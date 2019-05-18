from core.model.base import Base

class ContactType(object):
    TECHNICAL = 'TECHNICAL'
    BUSINESS = 'BUSINESS'

class Contact(Base):
    def __init__(self):
        self.contact_name = None
        self.contact_type = None
        self.phone = None
        self.email = None


