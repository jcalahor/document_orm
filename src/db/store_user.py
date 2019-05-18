from util.json import to_collection_json, to_json




def store_user(logger, cursor, entity):
    try:
        sql = """
            execute dbo.StoreUser 
				@Id = ?,
				@FirstName = ?,
				@LastName = ?,
				@Email = ?
        """
        params =  (entity.id,
            entity.first_name,
            entity.last_name,
            entity.email)            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while storing...")
        logger.error(e)
        raise
