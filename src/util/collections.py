def to_numeric_collection(flat_collection):
    return [int(item) for item in flat_collection.split(',')]

def to_string_colllection(flat_collection):
    return flat_collection.split(',')

def to_string_flat_collection(collection):
    return ','.join(collection)

def to_numeric_flat_collection(collection):
    return ','.join(map(str, collection))

