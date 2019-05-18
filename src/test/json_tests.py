import datetime
import unittest
from util.json import to_collection_items, to_collection_json
from core.model.background import WorkBackground
from config.config import init

JSON_TEST_STR = '[[{"Type": "WorkBackground"}, {"start_date": "2019-04-02 00:00:00", "position": "manager", "business_name": "signum", "business_address": "artigas", "phone_number": "22333", "email_contact": "jcalahor@ya.com", "salary": 10000, "is_verified": false, "file_attachments": ""}], [{"Type": "WorkBackground"}, {"start_date": "2019-04-02 00:00:00", "position": "manager2", "business_name": "signum2", "business_address": "artigas2", "phone_number": "22333", "email_contact": "jcalahor2@ya.com", "salary": 10000, "is_verified": false, "file_attachments": ""}]]'

class FileItem(object):
    def __init__(self):
        self.fname = 'sfdsdf'
        self.dummy1 = 10
        self.dummy2 = datetime.datetime.now()

class Guaido(object):
    def __init__(self):
        self.xname = 'sdfsdffdssdf'
        self.dummy10 = 10

class DBTests(unittest.TestCase):
    def test_serialize(self):
        init()
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

        json_data = to_collection_json([wb, wb2])

        print (json_data)
        print (JSON_TEST_STR)
        self.assertTrue(json_data == JSON_TEST_STR)

        items = to_collection_items(json_data)
        self.assertTrue(items[0].position == 'manager')
        self.assertTrue(items[1].position == 'manager2')







