def delete_externaluser(logger, cursor, entity):
    try:
        sql = """
            execute dbo.DeleteExternalUser 
				@Id = ?
        """
        params =  (entity.id
            )            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while deleting...")
        logger.error(e)
        raise
