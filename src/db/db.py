import pyodbc


def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)


class Db(object):
    def call_function(self, entity, prefix):
        if not hasattr(entity.__class__, 'UseParentforORM'):
            entity_name = entity.__class__.__name__.lower()
        else:
            entity_name = entity.__class__.__bases__[0].__name__.lower()
        function = import_from('db.' + prefix + '_' + entity_name, prefix + '_' + entity_name)
        function(self.logger, self.cursor, entity)

    def call_get_function(self, class_type, filter_sql):
        if not hasattr(class_type, 'UseParentforORM'):
            entity_name = class_type.__name__.lower()
        else:
            entity_name = class_type.__bases__[0].__name__.lower()
        func_name = 'get_' + entity_name + 's'
        function = import_from('db.' + func_name, func_name)
        return function(self.logger, self.connection, filter_sql)

    def __init__(self, connection_string, logger):
        self.connection_string = connection_string
        self.logger = logger
        self.cursor = None

    def open(self):
        self.connection = pyodbc.connect(self.connection_string)

    def close(self):
        self.connection.close()

    def store_entity(self, entity):
        self.call_function(entity, 'store')

    def delete_entity(self, entity):
        self.call_function(entity, 'delete')

    def get_entities(self, class_type, filter_sql):
        return self.call_get_function(class_type, filter_sql)

    def get_single_entity(self, class_type, filter_sql):
        entities = self.call_get_function(class_type, filter_sql)
        if len(entities) > 0:
            return entities[0]
        return None

    def start_cursor(self):
        self.cursor = self.connection.cursor()

    def terminate_cursor(self):
        self.cursor.commit()
        self.cursor.close()

    def store_single(self, entity):
        self.start_cursor()
        self.store_entity(entity)
        self.terminate_cursor()

    def delete_single(self, entity):
        self.start_cursor()
        self.delete_entity(entity)
        self.terminate_cursor()
