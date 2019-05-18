from util.json import to_collection_json, to_json




def store_externaluser(logger, cursor, entity):
    try:
        sql = """
            execute dbo.StoreExternalUser 
				@Id = ?,
				@FirstName = ?,
				@LastName = ?,
				@Email = ?,
				@CompanyName = ?,
				@MailingAddress = ?
        """
        params =  (entity.id,
            entity.first_name,
            entity.last_name,
            entity.email,
            entity.company_name,
            entity.mailing_address)            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while storing...")
        logger.error(e)
        raise
