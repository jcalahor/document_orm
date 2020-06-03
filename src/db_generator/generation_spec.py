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
    ('User', ['model.user', 'Base', 'User', EntityTableMapType.SINGLE,
              [
                  ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                  ('FirstName', 'varchar', 100, 'first_name', None, 'NOT NULL'),
                  ('LastName', 'varchar', 100, 'last_name', None, 'NOT NULL'),
                  ('Email', 'varchar', 100, 'email', None, 'NOT NULL'),
                  ('UserName', 'varchar', 100, 'user_name', None, 'NOT NULL'),
                  ('Password', 'varchar', 100, 'password', None, 'NOT NULL'),
                  ('Role', 'int', None, 'role', None, 'NULL'),
                  ('Avatar', 'int', None, 'avatar', None, 'NULL'),
                  ('Favorites', 'list|int', None, 'favorites', None, 'NULL')
              ]
             ]
     ),
    ('Announcement', ['model.announcement', 'Base', 'Announcement', EntityTableMapType.SINGLE,
              [
                  ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                  ('CreationDate', 'datetime', None, 'creation_date', None, 'NOT NULL'),
                  ('NewsLink',  'varchar', 528, 'news_link', None, 'NOT NULL')
              ]
             ]
     ),
    ('PlayaConfiguration', ['model.playa_configuration', 'Base', 'PlayaConfiguration', EntityTableMapType.SINGLE,
              [
                  ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                  ('SiteLogo', 'varchar', 256, 'site_logo', None, 'NOT NULL'),
                  ('SiteName', 'varchar', 256, 'site_name', None, 'NOT NULL'),
                  ('LobbyLogo', 'varchar', 256, 'lobby_logo', None, 'NOT NULL'),
                  ('Theme', 'int', None, 'theme', None, 'NULL'),
                  ('Categories', 'bit', None, 'categories', None, 'NULL'),
                  ('Announcements', 'bit', None, 'announcements', None, 'NULL'),
                  ('FreeVideos', 'bit', None, 'free_videos', None, 'NOT NULL'),
                  ('FreedVideoCategoryLogo',  'varchar', 256, 'lobby_logo', None, 'NOT NULL'),
                  ('Registry', 'bit', None, 'registry', None, 'NOT NULL')
              ]
             ]
     ),
    ('Category', ['model.category', 'Base', 'Category', EntityTableMapType.SINGLE,
              [
                  ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                  ('CategoryId',  'int', None, 'category_id', None, 'NULL'),
                  ('Name', 'varchar', 100, 'name', None, 'NOT NULL'),
                  ('Image', 'varchar', 256, 'image', None, 'NOT NULL')
              ]
             ]
     ),
    ('Video', ['model.video', 'Base', 'Video', EntityTableMapType.SINGLE,
              [
                  ('Id', 'UNIQUEIDENTIFIER', None, 'id', ['PK'], 'NOT NULL'),
                  ('VideoId',   'int', None,  'video_id', None, 'NOT NULL'),
                  ('DateGMT',  'varchar', 256, 'date_gmt', None, 'NOT NULL'),
                  ('Title',  'varchar', 256, 'title', None, 'NOT NULL'),
                  ('Status',  'varchar', 50, 'status', None, 'NOT NULL'),
                  ('Content',  'varchar', 1024, 'content', None, 'NOT NULL'),
                  ('VideoCategory',  'list|int', None, 'video_category', None, 'NOT NULL'),
                  ('VideoPoster',  'varchar', 1024, 'video_poster', None, 'NOT NULL'),
                  ('VideoPreviewSprite',  'varchar', 1024, 'video_preview_sprite', None, 'NOT NULL'),
                  ('TrailerPreviewSprite',  'varchar', 1024, 'trailer_preview_sprite', None, 'NOT NULL'),
                  ('VideoLinks',  'dict', None, 'video_links', None, 'NOT NULL'),
                  ('TrailerLinks',  'dict', None, 'trailer_links', None, 'NOT NULL'),
                  ('VideoPositions',  'list|string', None, 'video_positions', None, 'NOT NULL'),
                  ('VideoRating', 'int', None,  'video_rating', None, 'NOT NULL'),
                  ('VideoFeatured',  'int', None, 'video_featured', None, 'NOT NULL'),
                  ('VideoDuration',  'varchar', 10, 'video_duration', None, 'NOT NULL'),
                  ('VideoFPS',  'varchar', 10, 'video_fps', None, 'NOT NULL'),
                  ('VideoStarring',  'list|string', None, 'video_starring', None, 'NOT NULL'),
                  ('VideoTags',  'list|string', None, 'video_tags', None, 'NOT NULL'),
                  ('SeekMarkersFull',  'list|string', None, 'seek_markers_full', None, 'NOT NULL'),
                  ('SeekMarkersTrailer',  'list|string', None, 'seek_markers_trailer', None, 'NOT NULL'),
                  ('TimeCodesForTrailer',  'list|int', None, 'timecodes_for_trailer', None, 'NOT NULL'),
                  ('TimeCodesForVideo',  'list|int', None, 'timecodes_for_video', None, 'NOT NULL'),
                  ('AutomaticCameraTilt',  'JSON', None, 'automatic_camera_tilt', None, 'NOT NULL'),
                  ('AutomaticCameraTiltTrailer',  'JSON', None, 'automatic_camera_tilt_trailer', None, 'NOT NULL'),
                  ('Description',  'varchar', 256, 'description', None, 'NOT NULL')                
              ]
             ]
     ),
    ]

REFERENCE_SPEC = [
]

CHILD_ENTITY_JSON_DATA = { 
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