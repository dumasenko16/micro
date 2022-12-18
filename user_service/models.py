import mongoengine
import config
import utils as hashing


class User(mongoengine.Document):
    meta = {
        'db_alias': config.DB_NAME,
        'collection': config.COLLECTION_NAME
    }

    user_uuid = mongoengine.UUIDField(primary_key=True)
    username = mongoengine.StringField(max_length=200, required=True)
    email = mongoengine.StringField(max_length=200, required=True)
    password = mongoengine.StringField(max_length=200, required=True)

    def check_password(self, password):
        return hashing.verify_password(self.password, password)
