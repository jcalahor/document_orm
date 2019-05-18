from util.json import to_collection_json, to_json

from core.model.source.email_source import EmailSource
from core.model.source.ftp_source import FTPSource

def additional_fields_to_json(entity):
    json_map = dict()
    if type(entity) == EmailSource:                
        json_map["SenderEmail"] = entity.sender_email
        json_map["SubjectPattern"] = entity.subject_pattern
    elif type(entity) == FTPSource:                
        json_map["FTPHost"] = entity.ftp_host
        json_map["FTPUserName"] = entity.ftp_username
        json_map["FTPPassword"] = entity.ftp_password
        json_map["FTPLocation"] = entity.ftp_location
    return to_json(json_map)


def store_entlsource(logger, cursor, entity):
    try:
        sql = """
            execute dbo.StoreEntlSource 
				@Id = ?,
				@EntlType = ?,
				@SourcePath = ?,
				@DetailData = ?
        """
        params =  (entity.id,
            entity.entl_type,
            entity.source_path,
            additional_fields_to_json(entity))            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while storing...")
        logger.error(e)
        raise
