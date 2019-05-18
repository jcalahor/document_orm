from util.json import to_collection_items, to_object
import importlib

from core.model.source.email_source import EmailSource
from core.model.source.ftp_source import FTPSource
from core.model.source.entl_source import EntlSource

    
def get_entlsources(logger, connection, filter_sql):
    entities = []
    
    module_map = {'EmailSource':'core.model.source.email_source', 'FTPSource':'core.model.source.ftp_source', }
    
    def read(row):
        module = importlib.import_module(module_map[row[2]])
        class_ = getattr(module, row[2])
        entity = class_()
        
        entity.id = row[0]
        entity.entl_type = row[1]
        entity.source_path = row[2]
        json_map =  to_object(row[3])

        if type(entity) == EmailSource:                
            entity.sender_email = json_map["SenderEmail"]
            entity.subject_pattern = json_map["SubjectPattern"]
        elif type(entity) == FTPSource:                
            entity.ftp_host = json_map["FTPHost"]
            entity.ftp_username = json_map["FTPUserName"]
            entity.ftp_password = json_map["FTPPassword"]
            entity.ftp_location = json_map["FTPLocation"]
        entities.append(entity)
    try:         
        cursor = connection.cursor()
        sql = "execute dbo.GetEntlSources @filter = ?"
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
