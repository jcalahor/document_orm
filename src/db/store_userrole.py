from util.json import to_collection_json, to_json




def store_userrole(logger, cursor, entity):
    try:
        sql = """
            execute dbo.StoreUserRole 
				@Id = ?,
				@RoleId = ?,
				@UserId = ?,
				@LoginName = ?
        """
        params =  (entity.id,
            entity.role_id,
            entity.user_id,
            entity.login_name)            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while storing...")
        logger.error(e)
        raise
