from util.json import to_collection_items, to_object
import importlib

from core.model.system import System

    
def get_systems(logger, connection, filter_sql):
    entities = []
    
    
    def read(row):
        entity = System()
        entity.id = row[0]
        entity.system_name = row[1]
        entity.system_description = row[2]
        entity.contacts = to_collection_items(row[3])
        entities.append(entity)
    try:         
        cursor = connection.cursor()
        sql = "execute dbo.GetSystems @filter = ?"
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
