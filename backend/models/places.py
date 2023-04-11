from mongoengine import Document,ListField,StringField, URLField, DictField,IntField,ReferenceField


from users import UserSchema

class PlaceSchema:
  title=StringField(required=True)
  description=StringField(required=True)
  address=StringField(required=True)
  location=DictField({
    'lat': IntField(required=True),
    'lon': IntField(required=True),
  })
  image=StringField(required=True)
  creatorId=ReferenceField(UserSchema,required=True)

