from util.json import to_collection_items, to_object
import importlib

from core.model.role import Role

    
def get_roles(logger, connection, filter_sql):
    entities = []
    
    
    def read(row):
        entity = Role()
        entity.id = row[0]
        entity.system_id = row[1]
        entity.role_name = row[2]
        entity.role_description = row[3]
        entities.append(entity)
    try:         
        cursor = connection.cursor()
        sql = "execute dbo.GetRoles @filter = ?"
        params = (filter_sql)            
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        list(map(read, rows))
        cursor.close()
        return entities
    except Exception as e:
        logger.error("error while getting staging entities...")
        logger.error(e)
        raise
