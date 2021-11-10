from mongoengine import Document, fields

# Create your models here.
class Users(Document):
    meta = {"collection" : "users"}
    # UserId = fields.IntField(max_length=500)
    hospital = fields.StringField(max_length=500)
    phone = fields.StringField(max_length=500)
    role = fields.StringField(max_length=500)
    profile_pic = fields.StringField(max_length=500)
    email = fields.StringField(max_length=500)
    name = fields.StringField(max_length=500)
    date = fields.StringField(max_length=500)