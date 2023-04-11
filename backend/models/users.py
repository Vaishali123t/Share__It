

from mongoengine import StringField,ReferenceField

from places import PlaceSchema

class UserSchema:
    name=StringField(required=True)
    email= StringField(required=True, unique=True)
    password= StringField(required=True, min_length=6)
    image= StringField(required=True)
    places= [ReferenceField(PlaceSchema,required=True)]

