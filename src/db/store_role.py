from util.json import to_collection_json, to_json




def store_role(logger, cursor, entity):
    try:
        sql = """
            execute dbo.StoreRole 
				@Id = ?,
				@SystemId = ?,
				@RoleName = ?,
				@RoleDecription = ?
        """
        params =  (entity.id,
            entity.system_id,
            entity.role_name,
            entity.role_description)            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while storing...")
        logger.error(e)
        raise
