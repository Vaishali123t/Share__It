import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson.json_util import dumps
import json
from bson import json_util
from bson.objectid import ObjectId


from globals import client
from models import http_error
from middlewares import file_upload
# from models.places import PlaceSchema
# from models.users import UserSchema
from util.location import getCoordsForAddress


def getPlaceById(placeId):

    db=client.Share_It
    collection_places=db.places
    place=''
    try:
        place_obj = collection_places.find_one( {'_id':ObjectId(oid=str(placeId))})
        place=dumps(place_obj)
    except Exception as e:
        # error= http_error.HttpException('Something went wrong. Could not find a place', 501)
        return {"message":"Something went wrong. Could not find a place"}


    if place=='' or place==None:
        # return (http_error.HttpException("Could not find place with the provided id.", 404))
        return {"message": "Could not find place with the provided id."}

    print(place)

    return {'place': place}


async def getPlacesByUserId(userId): #working

    db=client.Share_It
    collection_places=db.places
    allPlaces=[]
    try:
        allPlaces_obj =  collection_places.find( {'creatorId':ObjectId(oid=str(userId))})
        # print("collection_places-->",collection_places)
        allPlaces=list(allPlaces_obj)
    except Exception as e:
        # error = http_error.HttpException('Something went wrong. Could not find a place', 500)
        return {"message":"Something went wrong. Could not find a place"}

    # print("allPlaces", allPlaces)

    if (len(allPlaces) == 0):
        return {'places': []}
        # return next(http_error.HttpException("Could not find place with the provided userid.", 404))
        # return {"message": "Could not find place with the provided user id."}
    
    places_to_return=[]
    for place in allPlaces:
        place_dict = {}
        # print("place-->",place)
        place_dict['id']=str(place['_id'])
        place_dict['description']=str(place['description'])
        place_dict['title'] = list(place['title'])
        place_dict['image'] = str(place['image'])
        place_dict['creator'] = str(place['creatorId'])
        place_dict['location'] = (place['location'])
        places_to_return.append(place_dict)
        
    return  {'places':places_to_return}

async def createPlace(creator,title, description, address,file): # working

    try:
        file_name= file.filename
        print("file_path-->",file_name)
        # if file and allowed_file(file_path):
        status, file_uuid= file_upload.fileUpload(file,file_name)
        if not status:
            return {"message":"Could not save file"}
    except Exception as e:
        print("file path",e)
        return {"message":"Could not get file path"}

    db= client.Share_It
    collection_users=db.users
    collection_places=db.places

    coordinates = getCoordsForAddress(address)
    file_path=os.path.join('uploads\images', file_uuid)
    # createdPlace = PlaceSchema()
    # createdPlace.title=title
    # createdPlace.description = description
    # createdPlace.address = address
    # createdPlace.coordinates = coordinates
    # createdPlace.image = req.file.path
    # createdPlace.creatorId=creator
    createdPlace={'title':title,'description':description,'address':address,'location':coordinates,'image':file_path,'creatorId':ObjectId(creator)}

    user=''
    try:
        user = collection_users.find_one({'_id':ObjectId(oid=str(creator))})
    except Exception as e:
        return {"message": "Creating place failed. Please Try again."}
        # error = http_error.HttpException("Creating place failed. Please Try again.",500)
        # return error

    if user=='' or user==None:
        # error = http_error.HttpException("Could not find the user with this id.",404)
        return {"message": "Could not find the user with this id."}

    try:
        placeCreated= collection_places.insert_one(createdPlace) # place inserted in places collection
        user["places"].append(placeCreated.inserted_id) # put the same place in our places lit variable
        updatedUser = {'name': user["name"],'email': user["email"],'image': file_path,'password': user["password"],'places': user["places"]}
        collection_users.replace_one({'_id':user["_id"]},updatedUser)

    except Exception as e:
        # error= http_error.HttpException('Creating place failed. Please Try again.',500)
        return {"message": "Creating place failed. Please Try again."}

    return dumps(createdPlace)  # working

async def editPlaceById(placeid,title,description,current_user): # working
    db=client.Share_It
    collection_places=db.places
    collection_users=db.users

    place=''
    try:
        place = collection_places.find_one({'_id':ObjectId(oid=str(placeid))})
        creatorId = place["creatorId"]
    except Exception as e:
        # error = http_error.HttpException("Something went wrong. Could not find a place with this id",500)
        return {"message": "Something went wrong. Could not find a place with this id."}


    if (str(creatorId) != str(current_user)):
        # error = http_error.HttpException('You are not allowed to edit this place.', 401)
        return {"message": "You are not allowed to edit this place."}

    place["title"] = title
    place["description"] = description

    try:
        # await place.save()
        collection_places.replace_one({'_id': ObjectId(oid=str(placeid))}, place)
    except Exception as e:
        # error= http_error.HttpException('Something went wrong. Could not update place.', 500)
        return {"message": "Something went wrong. Could not update place."}

    return dumps({'place': place})

async def deletePlaceById(placeId): # working

    current_user = get_jwt_identity()
    db=client.Share_It
    collection_places=db.places
    collection_users=db.users
    place=''
    try:
        place = collection_places.find_one({'_id':ObjectId(oid=str(placeId))})
    except Exception as e:
        # error = http_error.HttpException("Something went wrong. Could not find a place with this id.",500)
        return {"message": "Something went wrong. Could not find a place with this id."}

    if(place=='' or place==None):
        return {"message": "Something went wrong. Could not find a place with this id."}

    try:
        creatorId = place["creatorId"]
        creator = collection_users.find_one({'_id': ObjectId(oid=str(creatorId))})
        creator_name = creator["name"]
    except:
        return {"message": "Something went wrong. Could not find a creator for this place."}

    if (str(creatorId) != str(current_user)):
        # error = http_error.HttpException('You are not allowed to edit this place.', 401)
        return {"message": "You are not allowed to delete this place."}
    
    imagePath= place["image"]

    try:
        # sess = await mongoose.startSession()`
        # sess.startTransaction()
        # await place.remove({ session: sess })
        # place.creatorId.places.pull(place)
        # find places of the creator first
        allPlacesByCreator=creator["places"]
        allPlacesByCreator_afterDeletion=[]
        for p in list(allPlacesByCreator):  # iterating on a copy since removing will mess things up
            if p != place["_id"]:
                allPlacesByCreator_afterDeletion.append(p)

        creator["places"]=allPlacesByCreator_afterDeletion

        collection_users.replace_one({'_id': ObjectId(oid=str(creatorId))}, creator)
        # await place.creatorId.save({session:sess})
        # await sess.commitTransaction()
    except Exception as e:
        # error = http_error.HttpException("Creating place failed. Please Try again.",500)
        return {"message": "Creating place failed. Please Try again."}


    try:
        collection_places.delete_one({'_id':ObjectId(oid=str(placeId))})
    except Exception as e:
        # error= http_error.HttpException('Something went wrong. Could not delte place.',500)
        return {"message": "Something went wrong. Could not delte place."}

    os.remove(imagePath)
    # fs.unlink(imagePath,(esrr)=>{
    # console.log(err)
    # })
    return {'message':'place deleted'}

