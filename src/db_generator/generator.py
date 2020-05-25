import sys,os
sys.path.append(os.getcwd())
sys.path.append('/home/jcalahor/development/vr/vr_content_server/src')

from configparser import ConfigParser
import logging
import logging.config
import os
import pyodbc
from db_generator.db import Db
from db_generator.generation_spec import GENERATION_SPEC, get_parent_class, get_table_name, get_table_spec, REFERENCE_SPEC
from db_generator.sql_builder import build_create_table_sql, build_store_sp_sql, build_delete_sp_sql, build_get_sp_sql
from db_generator.python_src_builder import build_store_entity, build_delete_entity, build_get_entity


def get_entity_keys():
    entity_keys = {}
    classes = []
    for class_name in GENERATION_SPEC.keys():
        parent_class = get_parent_class(class_name)
        table_name = get_table_name(class_name)
        table_field_spec = get_table_spec(class_name)

        classes = [class_name] + classes
        pk_field_list = [field_spec for field_spec in table_field_spec if field_spec[4] and field_spec[4][0] == 'PK']

        field_name, field_type, size, member_name, index_type, null_spec = (None, None, None, None, None, None)
        if (len(pk_field_list) == 1):
            field_name, field_type, size, member_name, index_type, null_spec = pk_field_list[0]
        entity_keys[class_name] = (table_name, parent_class, (field_name, field_type, size, member_name, index_type, null_spec))
    return entity_keys, classes


def process_spec(db, logger, python_target_folder):
    def create_references():
        # references
        for ref_spec in REFERENCE_SPEC:
            source_info, target_info = ref_spec

            source_table, source_field = source_info
            target_table, target_field = target_info

            sql_constraint = """ALTER TABLE [{0}]  WITH CHECK ADD  CONSTRAINT [FK_{0}_{1}] FOREIGN KEY([{2}])
                            REFERENCES [{1}] ([{3}])  
                        ALTER TABLE [{0}] CHECK CONSTRAINT [FK_{0}_{1}]""".format(target_table, source_table,
                                                                                  target_field, source_field)
            db.execute(sql_constraint)

    def clear_db_objects(classes):
        for class_name in classes:
            table_name = get_table_name(class_name)
            sql_drop  = "if exists (select * from sys.objects where name = '{0}' and type = 'u') drop table [{1}] ".format(table_name, table_name)
            db.execute(sql_drop)
            sql_drop = "if exists (select * from sys.objects where name = 'Store{0}' and type = 'P') drop procedure Store{1} ".format(table_name, table_name)
            db.execute(sql_drop)
            sql_drop = "if exists (select * from sys.objects where name = 'Delete{0}' and type = 'P') drop procedure Delete{1} ".format(table_name, table_name)
            db.execute(sql_drop)
            sql_drop = "if exists (select * from sys.objects where name = 'Get{0}s' and type = 'P') drop procedure Get{1}s ".format(
                table_name, table_name)
            db.execute(sql_drop)

    def process_entity(entity_keys, class_name):
        def create_table(hierarchy):
            table_name = get_table_name(class_name)

            sql, secondary_indexes = build_create_table_sql(hierarchy, entity_keys, class_name)
            db.execute(sql)

            # secondry indexes
            if len(secondary_indexes) > 0:
                for sec_index_info in secondary_indexes:
                    field_name, unique_spec = sec_index_info
                    sql = """CREATE {0} NONCLUSTERED INDEX[IX_{1}] ON [{2}]
                    (
                        [{1}]
                    ASC
                    )WITH(PAD_INDEX=OFF, STATISTICS_NORECOMPUTE=OFF, SORT_IN_TEMPDB=OFF, DROP_EXISTING=OFF, ONLINE=OFF,
                          ALLOW_ROW_LOCKS=ON, ALLOW_PAGE_LOCKS=ON)
                    ON[PRIMARY]""".format('UNIQUE' if  unique_spec == 'U' else '', field_name, table_name)
                    db.execute(sql)

            # constraint for child tables
            if (len(hierarchy) > 1):
                parent_table, parent_class, (field_name, field_type, size, member_name, index_type, null_spec) = entity_keys[hierarchy[0]]
                sql_constraint = """ALTER TABLE [{0}]  WITH CHECK ADD  CONSTRAINT [FK_{0}_{1}] FOREIGN KEY([{2}])
                    REFERENCES [{1}] ([{2}])  
                ALTER TABLE [{0}] CHECK CONSTRAINT [FK_{0}_{1}]""".format(table_name, parent_table, field_name)
                db.execute(sql_constraint)



        def create_store_sp(hierarchy):
            sql = build_store_sp_sql(hierarchy, entity_keys)
            db.execute(sql)

        def create_delete_sp(hierarchy):
            sql = build_delete_sp_sql(hierarchy, entity_keys, class_name)
            db.execute(sql)

        def create_get_sp(hierarchy):
            sql = build_get_sp_sql(hierarchy, entity_keys, class_name)
            db.execute(sql)

        def create_python_src_store():
            python_code = build_store_entity(class_name, hierarchy)
            with open(python_target_folder + "/" + 'store_' + class_name.lower() + ".py", "w") as text_file:
                text_file.write(python_code)

        def create_python_src_delete():
            python_code = build_delete_entity(class_name, entity_keys, hierarchy)
            with open(python_target_folder + "/" + 'delete_' + class_name.lower() + ".py", "w") as text_file:
                text_file.write(python_code)

        def create_python_src_get():
            python_code = build_get_entity(class_name, hierarchy)
            with open(python_target_folder + "/" + 'get_' + class_name.lower() + "s.py", "w") as text_file:
                text_file.write(python_code)

        hierarchy = []
        current_class = class_name
        while (current_class != 'Base'):
            parent_table, parent_class, field_spec = entity_keys[current_class]
            hierarchy = [current_class] + hierarchy
            current_class = parent_class

        create_table(hierarchy)
        create_store_sp(hierarchy)
        create_delete_sp(hierarchy)
        create_get_sp(hierarchy)
        create_python_src_store()
        create_python_src_delete()
        create_python_src_get()

    entity_keys, classes = get_entity_keys()

    clear_db_objects(classes)

    for class_name in GENERATION_SPEC.keys():
        process_entity(entity_keys, class_name)

    create_references()


def run():
    logger = None
    try:
        parser = ConfigParser()
        logging.config.fileConfig('db_generator/db_generator.cfg')
        logger = logging.getLogger('basic')
        parser.read('db_generator/db_generator.cfg')
        logger.info("Starting generation process...")

        connection_string = parser.get('Db', 'connection_string')
        python_src_target = parser.get('python', 'target_folder')

        db = Db(connection_string, logger)
        db.open()

        process_spec(db, logger, python_src_target)

        db.close()
        logger.info("Ending")
    except Exception as e:
        logger.exception("Error while generating ...")


if __name__ == '__main__':
    run()
