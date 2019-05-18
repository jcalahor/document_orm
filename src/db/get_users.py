from util.json import to_collection_items, to_object
import importlib

from core.model.user import User

    
def get_users(logger, connection, filter_sql):
    entities = []
    
    
    def read(row):
        entity = User()
        entity.id = row[0]
        entity.first_name = row[1]
        entity.last_name = row[2]
        entity.email = row[3]
        entities.append(entity)
    try:         
        cursor = connection.cursor()
        sql = "execute dbo.GetUsers @filter = ?"
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
