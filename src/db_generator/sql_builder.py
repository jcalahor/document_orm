from db_generator.generation_spec import GENERATION_SPEC, get_parent_class, get_table_name, get_table_spec


SERIALIZABLE_FIELDS = ['JSON', 'list|int', 'list|string', 'dict']

def build_create_table_sql(hierarchy, entity_keys, class_name):
    table_name = get_table_name(class_name)
    table_field_spec = get_table_spec(class_name)

    def build_field_sql(field_name, field_type, size, null_spec):
        if not size:
                return '\n\t[{0}] [{1}] {2},'.format(field_name, field_type, null_spec)
        return '\n\t[{0}] [{1}] ({2}) {3},'.format(field_name, field_type, size, null_spec)
    sql = "create table [{0}](".format(table_name)

    fields = ""
    primary_key = None
    secondary_indexes = []
    process_hierarchy = True
    for field_spec in table_field_spec:
        if process_hierarchy:
            if len(hierarchy) > 1:
                parent = hierarchy[0]
                parent_table, parent_class, (field_name, field_type, size, member_name, index_info, null_spec) = entity_keys[parent]
                fields = fields + build_field_sql(field_name, field_type, size, null_spec)
                secondary_indexes.append((field_name, 'U'))
            process_hierarchy = False
        field_name, field_type, size, member_name, index_info, null_spec = field_spec
        field_type, size = ('NVARCHAR', 'MAX') if field_type in SERIALIZABLE_FIELDS else (field_type, size)
        if index_info:
            if (index_info[0] == 'PK'):
                primary_key = (field_name, field_type, size, index_info, null_spec)
            elif (index_info[0] == 'SK'):
                secondary_indexes.append((field_name, index_info[1]))

        fields = fields + build_field_sql(field_name, field_type, size, null_spec)

    ## ther is a primary key
    pk_sql = ""
    if primary_key:
        pk_sql = '\nCONSTRAINT [PK_{0}] PRIMARY KEY CLUSTERED \n([{1}] ASC) \nWITH (PAD_INDEX=OFF,STATISTICS_NORECOMPUTE=OFF,IGNORE_DUP_KEY=OFF,ALLOW_ROW_LOCKS=ON,ALLOW_PAGE_LOCKS=ON) ON [PRIMARY]'.format(
            table_name, primary_key[0])
    sql = sql + fields + pk_sql + '\n) ON [PRIMARY]'
    return sql, secondary_indexes


def build_store_sp_sql(class_hierarchy, entity_keys):
    parent_table_name = class_hierarchy[0]

    def build_sql(class_name, level):
        table_name = get_table_name(class_name)
        table_field_spec = get_table_spec(class_name)
        params = ""
        update_part_sql = ""
        insert_params = ""
        insert_param_values = ""
        primary_key = ""

        if level > 0:
            parent_table, parent_class, (field_name, field_type, size, member_name, index_info, null_spec) = entity_keys[class_hierarchy[0]]
            update_part_sql = update_part_sql + '[{0}] = @{1}, '.format(field_name, field_name)
            insert_params = insert_params + '[{0}], '.format(field_name)
            insert_param_values = insert_param_values + '@{0}, '.format(field_name)
            primary_key = field_name

        for field_spec in table_field_spec:
            field_name, field_type, size, member_name, index_info, null_spec = field_spec
            field_type, size = ('NVARCHAR', 'MAX') if field_type in SERIALIZABLE_FIELDS else (field_type, size)
            if index_info:
                if (index_info[0] == 'PK'):
                    primary_key = field_name
            if not size:
                params = params + '@{0} as [{1}], '.format(field_name, field_type)
            else:
                params = params + '@{0} as [{1}] ({2}), '.format(field_name, field_type, size)

            update_part_sql = update_part_sql + '[{0}] = @{1}, '.format(field_name, field_name)
            insert_params = insert_params + '[{0}], '.format(field_name)
            insert_param_values = insert_param_values + '@{0}, '.format(field_name)

        update_part_sql = update_part_sql[:-2]
        insert_params = insert_params[:-2]
        insert_param_values = insert_param_values[:-2]
        update_sql = "\n\t\tupdate [{0}] set {1} where [{2}] = @{2}".format(table_name, update_part_sql, primary_key)
        insert_sql = """\n\t\tinsert into [{0}] ({1})
        values ({2})""".format(table_name, insert_params, insert_param_values)

        return params, update_sql, insert_sql, primary_key

    sql = """create procedure Store{0}({1}) as
set nocount on
BEGIN TRY
    BEGIN TRAN
	    if exists(select * from [{0}] where [{2}] = @{2})
	    begin
		    {3}
	    end
	    else
	    begin
		    {4}
	    end
    COMMIT TRAN
END TRY
BEGIN CATCH
    IF(@@TRANCOUNT > 0)
        ROLLBACK TRAN;
    THROW; 
END CATCH
    """
    params = ""
    update_sql = ""
    insert_sql = ""
    primary_key = ""
    level = 0
    for class_name in class_hierarchy:
        sql_parts = build_sql(class_name, level)
        params = params + sql_parts[0]
        update_sql = update_sql + sql_parts[1]
        insert_sql = insert_sql + sql_parts[2]
        if level == 0:
            primary_key = sql_parts[3]
        level = level + 1

    params = params[:-2]
    sql = sql.format(get_table_name(class_name), params, primary_key, update_sql, insert_sql)

    return sql



def build_delete_sp_sql(class_hierarchy, entity_keys, class_name):
    table_name = get_table_name(class_name)
    sql = """create procedure Delete{0}({1}) as 
set nocount on
BEGIN TRY
    BEGIN TRAN
        {2}
    COMMIT TRAN
END TRY
BEGIN CATCH
    IF(@@TRANCOUNT > 0)
        ROLLBACK TRAN;
    THROW; 
END CATCH
    """
    params = ""
    primary_key = ""
    delete_sql = ""
    parent_table, parent_class, (field_name, field_type, size, member_name, index_info, null_spec) = entity_keys[class_hierarchy[0]]
    field_type, size = ('NVARCHAR', 'MAX') if field_type in SERIALIZABLE_FIELDS else (field_type, size)
    if not size:
        params = '@{0} as [{1}]'.format(field_name, field_type)
    else:
        params = '@{0} as [{1}] ({2})'.format(field_name, field_type, size)

    for class_name in class_hierarchy:
        tbl = get_table_name(class_name)
        delete_sql =  "\n\t\tdelete from [{0}] where [{1}] = @{1}".format(tbl, field_name) + delete_sql

    sql = sql.format(table_name, params, delete_sql)
    return sql


def build_get_sp_sql(hierarchy_class, entity_keys, class_name):
    sql = """create procedure Get{0}s(@filter as nvarchar(256))
    as
    set nocount on
    declare @sql nvarchar(4000)
	set  @sql = N'select {1} from {2} where ' + @filter

    {3}

	insert into #temp_{4} execute sp_executesql  @sql
	select * from #temp_{4}
	drop table #temp_{4}    
    """

    parent_table, parent_class, (field_name, field_type, size, member_name, index_info, null_spec) = entity_keys[hierarchy_class[0]]
    primary_key = field_name
    table_name = get_table_name(class_name)

    fields = ""
    fields_temp_table = ""
    for cls in hierarchy_class:
        table_field_spec = get_table_spec(cls)
        for field_spec in table_field_spec:
            field_name, field_type, size, member_name, index_info, null_spec = field_spec
            field_type, size = ('NVARCHAR', 'MAX') if field_type in SERIALIZABLE_FIELDS else (field_type, size)
            if not size:
                fields_temp_table = fields_temp_table + '\n\t[{0}] [{1}],'.format(field_name, field_type)
            else:
                fields_temp_table = fields_temp_table + '\n\t[{0}] [{1}] ({2}),'.format(field_name, field_type, size)

            fields = fields + '[' + get_table_name(cls) + '].' + field_name + ', '
    fields = fields[:-2]

    inner_joins = ""
    for i in range(1, len(hierarchy_class)):
        tbl = get_table_name(hierarchy_class[i])
        inner_joins = inner_joins + "\n\t\tinner join [{0}] on [{0}].{1} = [{2}].{1}".format(tbl, primary_key, parent_table)

    table_sql = "create table #temp_{0}(".format(table_name)
    table_sql = table_sql + fields_temp_table[:-1] + ')'
    sql = sql.format(table_name, fields, '[' + parent_table + '] ' + inner_joins, table_sql, table_name)
    return sql


