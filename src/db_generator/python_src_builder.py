from db_generator.generation_spec import GENERATION_SPEC, get_parent_class, get_table_name, get_table_spec, get_module_name, EntityTableMapType, get_entity_table_map_type, get_composite_map_spec


def build_store_entity(entity, class_hierarchy):
    table_name = get_table_name(entity)
    python_src = """from util.json import to_collection_json, to_json
from util.collections import to_numeric_collection, to_string_colllection, to_string_flat_collection, to_numeric_flat_collection
import json

{0}

{1}

def store_{2}(logger, cursor, entity):
    try:
        sql = \"\"\"
            {3}
        \"\"\"
        params =  ({4})            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while storing...")
        logger.error(e)
        raise
"""

    python_src_composite_map = """def additional_fields_to_json(entity):
    json_map = dict(){0}
    return to_json(json_map)
"""
    import_map_src = ""
    if get_entity_table_map_type(class_hierarchy[0]) == EntityTableMapType.COMPOSITE:
        _, _, package_map = get_composite_map_spec(table_name)[0]
        for key in package_map:
            import_map_src = import_map_src + '\nfrom {0} import {1}'.format(package_map[key], key)

    params = ""
    param_values = ""

    for class_name in class_hierarchy:
        member_spec = get_table_spec(class_name)
        for field_spec in member_spec:
            field_name, field_type, size, member_name, index_info, null_spec = field_spec
            params = params + '\n\t\t\t\t@{0} = ?,'.format(field_name)
            if member_name != "_":
                if field_type == 'list|int':
                    param_values = param_values + 'to_numeric_flat_collection(entity.{0}),\n            '.format(member_name)
                elif field_type ==  'list|string':
                    param_values = param_values + 'to_string_flat_collection(entity.{0}),\n            '.format(member_name)
                elif field_type == 'dict':
                    param_values = param_values + 'json.dumps(entity.{0}),\n            '.format(member_name)
                elif field_type == 'JSON':
                    param_values = param_values + 'to_collection_json(entity.{0}),\n            '.format(member_name)
                else:
                    param_values = param_values + 'entity.{0},\n            '.format(member_name)
            else: ## is a composite
                param_values = param_values + 'additional_fields_to_json(entity),\n            '

    params = params[:-1]
    param_values = param_values[:-14]

    call_sp = "execute dbo.Store{0} {1}".format(entity, params)

    if get_entity_table_map_type(class_name) == EntityTableMapType.COMPOSITE:
        composite_src = ""
        composite_spec = get_composite_map_spec(table_name)[1]

        if_statement = 'if'
        for key in composite_spec:

            field_maps = ""
            for field_spec in composite_spec[key]:
                source_field, target_field = field_spec
                field_maps = field_maps + '        json_map["{0}"] = entity.{1}\n'.format(target_field, source_field)
            field_maps = field_maps[:-1]
            composite_src = composite_src + """\n    {0} type(entity) == {1}:                
{2}""".format(if_statement, key, field_maps)
            if_statement = 'elif'
        python_src_composite_map = python_src_composite_map.format(composite_src)
    else:
        python_src_composite_map = ""


    python_src = python_src.format(import_map_src, python_src_composite_map, entity.lower(), call_sp, param_values)
    return python_src


def build_delete_entity(entity, entity_keys, class_hierarchy):
    python_src = """def delete_{0}(logger, cursor, entity):
    try:
        sql = \"\"\"
            {1}
        \"\"\"
        params =  ({2})            
        cursor.execute(sql, params)
    except Exception as e:
        logger.error("error while deleting...")
        logger.error(e)
        raise
"""

    params = ""
    param_values = ""
    parent_table, parent_class, (field_name, field_type, size, member_name, index_info, null_spec) = entity_keys[class_hierarchy[0]]
    params = params + '\n\t\t\t\t@{0} = ?'.format(field_name)
    param_values = param_values + 'entity.{0}\n            '.format(member_name)

    call_sp = "execute dbo.Delete{0} {1}".format(entity, params)
    python_src = python_src.format(entity.lower(), call_sp, param_values)
    return python_src


def build_get_entity(entity, class_hierarchy):
    def build_composite_additional_fields_src(class_name, table_name, i):
        composite_src = ""
        if get_entity_table_map_type(class_name) == EntityTableMapType.COMPOSITE:

            json_map_src = "\n        json_map =  to_object(row[{0}])\n".format(str(i))
            composite_spec = get_composite_map_spec(table_name)[1]

            if_statement = '    if'
            for key in composite_spec:
                field_maps = ""
                for field_spec in composite_spec[key]:
                    source_field, target_field = field_spec
                    field_maps = field_maps + '            entity.{0} = json_map["{1}"]\n'.format(source_field, target_field)
                field_maps = field_maps[:-1]
                composite_src = composite_src + """\n    {0} type(entity) == {1}:                
{2}""".format(if_statement, key, field_maps)
                if_statement = '    elif'
        return json_map_src + composite_src

    table_name = get_table_name(entity)
    python_src = """from util.json import to_collection_items, to_object
from util.collections import to_numeric_collection, to_string_colllection, to_string_flat_collection, to_numeric_flat_collection
import importlib
{0}
from {1} import {2}

    
def get_{3}s(logger, connection, filter_sql):
    entities = []
    {4}
    
    def read(row):
        {5}
    try:         
        cursor = connection.cursor()
        sql = "execute dbo.Get{6}s @filter = ?"
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
"""

    import_map_src = ""
    if get_entity_table_map_type(class_hierarchy[0]) == EntityTableMapType.COMPOSITE:
        _, _, package_map = get_composite_map_spec(table_name)[0]
        for key in package_map:
            import_map_src = import_map_src + '\nfrom {0} import {1}'.format(package_map[key], key)


    entry_map_src = ""
    modules_map_src = ""
    if get_entity_table_map_type(class_hierarchy[0]) == EntityTableMapType.COMPOSITE:
        _, _, package_map = get_composite_map_spec(table_name)[0]
        for key in package_map:
            entry_map_src = entry_map_src + "'{0}':'{1}', ".format(key, package_map[key])
        modules_map_src = "\n    module_map = {" + entry_map_src + "}"

    map_src = ""
    i = 0

    for class_name in class_hierarchy:
        member_spec = get_table_spec(class_name)
        for field_spec in member_spec:
            field_name, field_type, size, member_name, index_info, null_spec = field_spec
            if member_name != "_":
                if field_type == 'list|int':
                    map_src = map_src + "\n        entity.{0} = to_numeric_collection(row[{1}])".format(member_name, str(i))
                elif field_type ==  'list|string':
                    map_src = map_src + "\n        entity.{0} = to_string_colllection(row[{1}])".format(member_name, str(i))
                elif field_type == 'dict':
                    map_src = map_src + "\n        entity.{0} = json.load(row[{1}])".format(member_name, str(i))
                elif field_type == 'JSON':
                    map_src = map_src + "\n        entity.{0} = to_collection_items(row[{1}])".format(member_name, str(i))
                else:
                    map_src = map_src + "\n        entity.{0} = row[{1}]".format(member_name, str(i))
                    
            else: # composite process
                map_src = map_src + build_composite_additional_fields_src(class_name, table_name, i)
            i = i + 1

    if get_entity_table_map_type(class_name) == EntityTableMapType.COMPOSITE:
        _, index_type_entity, _ = get_composite_map_spec(table_name)[0]

        map_src = """module = importlib.import_module(module_map[row[{0}]])
        class_ = getattr(module, row[{0}])
        entity = class_()
        {1}\n        entities.append(entity)""".format(index_type_entity, map_src)
    else:
        map_src = "entity = {0}(){1}\n        entities.append(entity)".format(entity, map_src)
    python_src = python_src.format(import_map_src, get_module_name(class_name), entity, entity.lower(), modules_map_src, map_src, table_name)
    return python_src
