from util.json import to_collection_json, to_json




def store_system(logger, cursor, entity):
    try:
        sql = """
            execute dbo.StoreSystem 
				@Id = ?,
				@SystemName = ?,
				@SystemDescription = ?,
				@Contacts = ?
        """
        params =  (entity.id,
            entity.system_name,
            entity.system_description,
            to_collection_json(entity.contacts))            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while storing...")
        logger.error(e)
        raise
