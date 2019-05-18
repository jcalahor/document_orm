import pyodbc

class Db(object):
    def __init__(self, connection_string, logger):
        self.connection_string = connection_string
        self.logger = logger

    def open(self):
        self.connection = pyodbc.connect(self.connection_string)

    def close(self):
        self.connection.close()

    def execute(self, sql_command):
        self.logger.info("executing -> {}".format(sql_command))
        cur = self.connection.cursor()
        cur.execute(sql_command)
        self.connection.commit()


