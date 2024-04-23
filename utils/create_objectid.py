from bson import ObjectId


# Create an bson.ObjectId from a custom string
def create_objectid(s):
    return ObjectId(str(s).encode("utf-8").hex().zfill(24))
