def delete_role(logger, cursor, entity):
    try:
        sql = """
            execute dbo.DeleteRole 
				@Id = ?
        """
        params =  (entity.id
            )            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while deleting...")
        logger.error(e)
        raise
