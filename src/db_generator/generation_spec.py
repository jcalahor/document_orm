import collections

MODULE_NAME_IDX = 0
PARENT_CLASS_IDX = 1
TABLE_NAME_IDX = 2
ENTITY_TABLE_MAP = 3
FIELD_SPEC = 4

class EntityTableMapType(object):
    SINGLE = 'SINGLE'
    COMPOSITE = 'COMPOSITE'

GENERATION_SPEC = [
    ('User', ['core.model.user', 'Base', 'User', EntityTableMapType.SINGLE,
              [
                  ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                  ('FirstName', 'varchar', 100, 'first_name', None, 'NOT NULL'),
                  ('LastName', 'varchar', 100, 'last_name', None, 'NOT NULL'),
                  ('Email', 'varchar', 100, 'email', None, 'NOT NULL'),
              ]
              ]
     ),
    ('ExternalUser', ['core.model.external_user', 'User', 'ExternalUser', EntityTableMapType.SINGLE,
                 [
                     ('CompanyName', 'varchar', 100, 'company_name', None, 'NOT NULL'),
                     ('MailingAddress', 'varchar', 100, 'mailing_address', None, 'NOT NULL'),
                 ]
                 ]
     ),
    ('System', ['core.model.system', 'Base', 'System', EntityTableMapType.SINGLE,
               [
                   ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                   ('SystemName', 'varchar', 100, 'system_name', None, 'NOT NULL'),
                   ('SystemDescription', 'varchar', 100, 'system_description', None, 'NOT NULL'),
                   ('Contacts', 'JSON', None, 'contacts', None, 'NULL')
               ]
            ]
     ),
    ('Role', ['core.model.role', 'Base', 'Role', EntityTableMapType.SINGLE,
              [
                  ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                  ('SystemId', 'UNIQUEIDENTIFIER', None, 'system_id', ['SK', 'N'], 'NOT NULL'),
                  ('RoleName', 'varchar', 100, 'role_name', None, 'NOT NULL'),
                  ('RoleDecription', 'varchar', 1024, 'role_description', None, 'NOT NULL'),
              ]
            ]
     ),
    ('UserRole', ['core.model.user_role', 'Base', 'UserRole', EntityTableMapType.SINGLE,
               [
                   ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                   ('RoleId', 'UNIQUEIDENTIFIER', None, 'role_id', ['SK', 'N'], 'NOT NULL'),
                   ('UserId', 'UNIQUEIDENTIFIER', None, 'user_id', ['SK', 'N'], 'NOT NULL'),
                   ('LoginName', 'varchar', 100, 'login_name', None, 'NOT NULL'),
               ]
            ]
     ),
    ('EntlSource', ['core.model.source.entl_source', 'Base', 'EntlSource', EntityTableMapType.COMPOSITE,
                  [
                      ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                      ('EntlType', 'varchar', 100, 'entl_type', ['SK', 'N'], 'NOT NULL'),
                      ('SourcePath', 'varchar', 100, 'source_path', None, 'NOT NULL'),
                      ('DetailData', 'JSON', None, '_', None, 'NOT NULL'),
                  ]
              ]
     ),
]

REFERENCE_SPEC = [
    (('User', 'Id'), ('UserRole', 'UserId')),
    (('Role', 'Id'), ('UserRole', 'RoleId')),
    (('System', 'Id'), ('Role', 'SystemId')),
]

CHILD_ENTITY_JSON_DATA = {
    'EntlSource':
        [
            ('EntlType', 2, {'EmailSource':'core.model.source.email_source',
                                    'FTPSource':'core.model.source.ftp_source'}),
            {
                'EmailSource':[('sender_email', 'SenderEmail'), ('subject_pattern', 'SubjectPattern')],
                'FTPSource': [('ftp_host', 'FTPHost'), ('ftp_username', 'FTPUserName'), ('ftp_password', 'FTPPassword'), ('ftp_location', 'FTPLocation')],
            }
        ]
}


GENERATION_SPEC = collections.OrderedDict(GENERATION_SPEC)

def get_parent_class(class_name):
    return GENERATION_SPEC[class_name][PARENT_CLASS_IDX]

def get_module_name(class_name):
    return GENERATION_SPEC[class_name][MODULE_NAME_IDX]

def get_table_name(class_name):
    return GENERATION_SPEC[class_name][TABLE_NAME_IDX]

def get_table_spec(class_name):
    return GENERATION_SPEC[class_name][FIELD_SPEC]

def get_entity_table_map_type(class_name):
    return GENERATION_SPEC[class_name][ENTITY_TABLE_MAP]

def get_composite_map_spec(table):
    return CHILD_ENTITY_JSON_DATA[table]