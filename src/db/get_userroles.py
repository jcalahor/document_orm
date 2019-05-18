from util.json import to_collection_items, to_object
import importlib

from core.model.user_role import UserRole

    
def get_userroles(logger, connection, filter_sql):
    entities = []
    
    
    def read(row):
        entity = UserRole()
        entity.id = row[0]
        entity.role_id = row[1]
        entity.user_id = row[2]
        entity.login_name = row[3]
        entities.append(entity)
    try:         
        cursor = connection.cursor()
        sql = "execute dbo.GetUserRoles @filter = ?"
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
