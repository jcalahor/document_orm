import sys,os
sys.path.append(os.getcwd())
print (os.getcwd())
import unittest
from db.db import Db
from configparser import ConfigParser
import logging
import logging.config
import uuid
from config.config import init
from core.model.user import User
from core.model.system import System
from core.model.contact import Contact, ContactType
from core.model.external_user import ExternalUser
from core.model.role import Role
from core.model.user_role import UserRole
from core.model.source.email_source import EmailSource
from core.model.source.ftp_source import FTPSource
from core.model.source.entl_source import EntlType, EntlSource


def create_ftp_source():
    source = FTPSource()
    source.id = str(uuid.uuid4()).upper()
    source.entl_type = EntlType.FTP
    source.source_path = '/usr/loc1'
    source.ftp_host = 'host1'
    source.ftp_location = '/client1/feeds'
    source.ftp_password = '##$@'
    source.ftp_user_username = 'jcalah'
    return source

def create_email_source():
    source = EmailSource()
    source.id = str(uuid.uuid4()).upper()
    source.entl_type = EntlType.EMAIL
    source.source_path = '/usr/loc1'
    source.sender_email = 'vendor_serv@domain.com'
    source.subject_pattern = 'this is the data'
    return source

def create_user():
    user = User()
    user.id = str(uuid.uuid4()).upper()
    user.email = 'dummy@dummy.com'
    user.first_name = 'peter'
    user.last_name = 'johnson'
    return user

def create_contact(contact_type, contact_name, phone, email):
    contact = Contact()
    contact.id = str(uuid.uuid4()).upper()
    contact.contact_type = contact_type
    contact.contact_name = contact_name
    contact.phone = phone
    contact.email = email
    return contact

def create_external_user():
    user = ExternalUser()
    user.id = str(uuid.uuid4()).upper()
    user.email = 'dummy@dummy.com'
    user.first_name = 'peter'
    user.last_name = 'johnson'
    user.company_name = 'ABC'
    user.mailing_address = '1 ABC WAY 60125'
    return user

def create_system(system_name, system_description):
    system = System()
    system.system_name = system_name
    system.system_description = system_description
    system.id = str(uuid.uuid4()).upper()
    return system

def create_role(role_name, role_description, system_id):
    role = Role()
    role.id = str(uuid.uuid4()).upper()
    role.role_name = role_name
    role.role_description = role_description
    role.system_id = system_id
    return role

def create_user_role(roleid, userid, login_name):
    ur = UserRole()
    ur.id = str(uuid.uuid4()).upper()
    ur.role_id = roleid
    ur.user_id = userid
    ur.login_name = login_name
    return ur

class DBTests(unittest.TestCase):
    def setUp(self):
        init()
        self.parser = ConfigParser()
        logging.config.fileConfig('test/db_test.cfg')
        logger = logging.getLogger('basic')
        self.parser.read('test/db_test.cfg')
        connection_string = self.parser.get('Db', 'connection_string')
        self.db = Db(connection_string, logger)
        self.db.open()

    def tearDown(self):
        self.db.close()

    def test_role_user(self):
        user = create_user()
        system = create_system('system 1', 'this is system1')
        role = create_role('trader', 'can trade', system.id)
        ur = create_user_role(role.id, user.id, 'jcalah')

        self.db.store_single(system)
        self.db.store_single(role)
        self.db.store_single(user)
        self.db.store_single(ur)

        user_roles = self.db.get_entities(UserRole, "Id = '{0}'".format(ur.id))
        self.assertTrue(user_roles[0].id == ur.id)

        self.db.delete_single(ur)
        self.db.delete_single(user)
        self.db.delete_single(role)
        self.db.delete_single(system)

    def test_table_inheritance(self):
        user = create_external_user()
        self.db.store_single(user)

        users = self.db.get_entities(ExternalUser, "[ExternalUser].Id = '{0}'".format(user.id))
        self.assertTrue(users[0].id == user.id)

        self.db.delete_single(user)


    def test_collection(self):
        system = create_system('system 1', 'this is system1')
        contact1 = create_contact(ContactType.BUSINESS, 'peter stuart', '454-3332', 'email@domain.com')
        contact2 = create_contact(ContactType.TECHNICAL, 'andrew johnson', '454-33552', 'email2@domain2.com')
        system.contacts.append(contact1)
        system.contacts.append(contact2)
        self.db.store_single(system)

        systems = self.db.get_entities(System, "Id = '{0}'".format(system.id))
        self.assertTrue(systems[0].id == system.id)
        self.assertTrue(systems[0].contacts[0].contact_name == 'peter stuart')
        self.assertTrue(systems[0].contacts[1].contact_name == 'andrew johnson')

        self.db.delete_single(system)


    def test_inheritance_via_json(self):
        es = create_email_source()
        fs = create_ftp_source()

        self.db.store_single(es)
        self.db.store_single(fs)

        email_sources = self.db.get_entities(EmailSource, "Id = '{0}'".format(es.id))
        ftp_sources = self.db.get_entities(FTPSource, "Id = '{0}'".format(fs.id))

        self.assertTrue(email_sources[0].id == es.id)
        self.assertTrue(ftp_sources[0].id == fs.id)

        self.db.delete_single(es)
        self.db.delete_single(fs)
