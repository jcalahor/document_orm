import unittest
from db.db import Db
from configparser import ConfigParser
import logging
import logging.config
import uuid
import datetime
from config.config import init


def create_test_background():
    wb = WorkBackground()
    wb.start_date = datetime.datetime(2019, 4, 2, 0, 0)
    wb.position = "manager"
    wb.business_address = "artigas"
    wb.phone_number = "22333"
    wb.email_contact = "jcalahor@ya.com"
    wb.salary = 10000
    wb.is_verified = False
    wb.file_attachments = ""
    wb.business_name = "signum"

    wb2 = WorkBackground()
    wb2.start_date = datetime.datetime(2019, 4, 2, 0, 0)
    wb2.position = "manager2"
    wb2.business_address = "artigas2"
    wb2.phone_number = "22333"
    wb2.email_contact = "jcalahor2@ya.com"
    wb2.salary = 10000
    wb2.is_verified = False
    wb2.file_attachments = ""
    wb2.business_name = "signum2"
    return [wb, wb2]


def create_debtor():
    u = Debtor()
    # u.id = str(uuid.uuid4())
    u.id = "012B6774-A416-435E-B416-BB8BBA7833C1"
    u.first_name = "asdsad"
    u.last_name = "asdsad"
    u.user_name = "jcddddd"
    u.password = 'sdfs'
    u.user_role = "admin"
    u.rating_score = 10
    u.address1 = "perico de los palotes"
    u.address2 = ''
    u.address3 = ''
    u.phone = '3334222'
    u.dob = datetime.datetime.now()
    u.document_id = 'dc id 1'
    u.email = 'jcalahor@yahoo.com'
    u.is_enabled = True
    u.background_items = create_test_background()
    return u


class DBTests(unittest.TestCase):
    def setUp(self):
        init()
        self.parser = ConfigParser()
        logging.config.fileConfig('db_test.cfg')
        logger = logging.getLogger('basic')
        self.parser.read('db_test.cfg')
        connection_string = self.parser.get('Db', 'connection_string')
        self.db = Db(connection_string, logger)
        self.db.open()

    def tearDown(self):
        self.db.close()


    def test_storage_query_delete(self):
        debtor = create_debtor()
        self.db.start_cursor()
        self.db.store_entity(debtor)
        self.db.terminate_cursor()
        entities = self.db.get_entities(Debtor, "Debtor.Id = '012B6774-A416-435E-B416-BB8BBA7833C1'")
        self.assertTrue(entities[0].id == '012B6774-A416-435E-B416-BB8BBA7833C1')
        self.assertTrue(entities[0].background_items[0].position == 'manager')
        debtor.rating_score = 8
        debtor.background_items[0].position = 'managerx'
        self.db.start_cursor()
        self.db.store_entity(debtor)
        self.db.terminate_cursor()
        entities = self.db.get_entities(Debtor, "Debtor.Id = '012B6774-A416-435E-B416-BB8BBA7833C1'")
        self.assertTrue(entities[0].rating_score == 8)
        self.assertTrue(entities[0].background_items[0].position == 'managerx')

        self.db.start_cursor()
        self.db.delete_entity(entities[0])
        self.db.terminate_cursor()
        entities = self.db.get_entities(Debtor, "Debtor.Id = '012B6774-A416-435E-B416-BB8BBA7833C1'")
        self.assertTrue(len(entities) == 0)


    def test_storage_query_delete3(self):
        client = Client()
        client.id = str(uuid.uuid4()).upper()
        client.first_name = "jaime"
        client.last_name = "villicoral"
        client.user_name = 'petermhhh'
        client.password = '2pas'
        client.user_role = 'debtor'
        client.address1 = "perico de los palotes"
        client.address2 = ''
        client.address3 = ''
        client.phone = '3334222'
        client.dob = datetime.datetime.now()
        client.document_id = 'dc id 1'
        client.email = 'jcalahor@yahoo.com'
        client.is_enabled = True
        client.background_items = create_test_background()
        self.db.store_single(client)

        clients = self.db.get_entities(Client, "[Client].Id = '{0}'".format(client.id))
        self.assertTrue(clients[0].id == client.id)

        self.db.delete_single(clients[0])

    def test_storage_transactions(self):
        deposit = Deposit()
        deposit.id = "3f0f7c8e-41ee-452a-ac7a-75220e643776".upper()
        deposit.creation_date = datetime.datetime(2019, 4, 2, 0, 0)
        deposit.transaction_type = 'Deposit'
        deposit.last_update_date = datetime.datetime(2019, 4, 2, 0, 0)
        deposit.amount = 100
        deposit.state = 'new'
        deposit.reference = 'ref'
        deposit.fees = []
        deposit.effective_amount = 100
        deposit.total_commission = 100
        deposit.owner_id = '012B6774-A416-435E-B416-BB8BBA7833C1'

        self.db.store_single(deposit)

        deposits = self.db.get_entities(Deposit, "Id = '{0}'".format(deposit.id))
        self.assertTrue(deposits[0].id == deposit.id)



        self.db.delete_single(deposit)


    def test_storage_query_delete2(self):
        u = User()
        u.id = str(uuid.uuid4()).upper()
        u.first_name = "pablo"
        u.last_name = "villicoral"
        u.user_name = 'jcala'
        u.password = '2pas'
        u.user_role = 'admin'
        u.email = "jcalahor@yahoo.com"
        u.is_enabled = True

        self.db.store_single(u)

        users = self.db.get_entities(User, "[User].Id = '{0}'".format(u.id))
        self.assertTrue(users[0].id == u.id)

        ac = Account()
        ac.id = str(uuid.uuid4()).upper()
        ac.owner_id = u.id
        ac.cash_position = 0

        self.db.store_single(ac)

        accounts = self.db.get_entities(Account, "[Account].Id = '{0}'".format(ac.id))
        self.assertTrue(accounts[0].id == ac.id)

        l = Loan()
        l.id = str(uuid.uuid4()).upper()
        l.account_debtor_id = ac.id
        l.start_balance = 100
        l.start_date = datetime.datetime.now()
        l.payoff_date = datetime.datetime.now()
        l.interest_rate = 0.2
        l.balance = 80
        l.is_fully_allocated = False

        self.db.store_single(l)
        loans = self.db.get_entities(Loan, "[Loan].Id = '{0}'".format(l.id))
        self.assertTrue(loans[0].id == l.id)

        self.db.delete_single(loans[0])
        self.db.delete_single(accounts[0])
        self.db.delete_single(users[0])


