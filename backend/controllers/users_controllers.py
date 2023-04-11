import os
from flask_jwt_extended import create_access_token
from flask import jsonify
from bson.json_util import dumps
from os import environ
from bson import json_util
from bson.objectid import ObjectId

from globals import bcrypt
from globals import client
from models import http_error
from middlewares import file_upload
# from models.places import PlaceSchema
# from ..models.users import UserSchema


async def getAllUsers():
    db= client.Share_It
    collection=db.users
    users=''
    try:
        users_obj=  collection.find({})
        users=list(users_obj)
    except Exception as e:
        print(e)
        # error = http_error.HttpException("Fetching users failed. Please try again.", 500)
        return {"message": "Could not get users"}

    # res.status(200).json({'users': users.map(u= > u.toObject({getters: true}))}

    users_to_return=[]
    for user in users:
        user_dict = {}
        user_dict['id']=str(user['_id'])
        user_dict['name']=str(user['name'])
        user_dict['places'] = list(user['places'])
        user_dict['image'] = str(user['image'])
        users_to_return.append(user_dict)

    return dumps({'users':users_to_return})


async def getUserById(userId):

    db= client.Share_It
    collection=db.users
    hasUser=''
    try:
        hasUser_obj= await collection.find_one({'_id':ObjectId(oid=str(userId))})
        hasUser=dumps(hasUser_obj)
    except Exception as  e:
        return {"message": "Could not get users"}
        # error = http_error.HttpException("Some issue occured. Please try again.",500)
        # return next(error)
    if (hasUser=='' or hasUser==None):
        return  {"message": "User not found"}
        # return next(http_error.HttpException("User not found.", 404))
    return {'user': hasUser}



async def signUp(name, email, password,file): #working
    print(file)

    try:
        file_name= file.filename
        status, file_uuid= file_upload.fileUpload(file,file_name)
        if status==False:
            return {"message":"Could not save file"}
    except Exception as e:
        print("file path",e)
        return {"message":"Could not get file path"}

    db= client.Share_It
    collection=db.users
    hasUser=''
    try:
        hasUser= collection.find_one({'email':email})
        print("hauser",hasUser)
    except Exception as e:
        return {"message": "Signing up failed. Please try again."}
        # error = http_error.HttpException("Signing up failed. Please try again.",500)
        # return (error)

    if (hasUser!='' and hasUser!=None):
        # print("i am here?")
        return {"message": "Could not create user. Email Already exists!"}
        # return (http_error.HttpException("Could not create user. Email Already exists!", 422))

    hashedPassword=''

    try:
        hashedPassword= bcrypt.generate_password_hash(password).decode('utf-8')
        print("hashedPassword",hashedPassword)
    except Exception as e:
        print("error",e)
        # error = http_error.HttpException("Signing up failed. Please try again.", 500)
        return {"message": "Signing up failed. Please try again."}


    file_path=os.path.join('uploads\images', file_uuid)
    createdUser_dict={'name': name,'email': email,'image': file_path,'password': hashedPassword,'places': list()}

    try:
        userCreated_obj= collection.insert_one(createdUser_dict)
        # userCreated= dumps(userCreated_obj)
        print("userCreated",createdUser_dict)
    except Exception as e:
        # error = http_error.HttpException("Signing up failed. Please try again..", 500)
        return {"message": "Signing up failed. Please try again."}

    token=''
    try:
        token = create_access_token(identity=str(createdUser_dict['_id']))  # create jwt token
        print("token",token)
    except Exception as e:
        return {"message": "Signing up failed. Please try again."}
    print({'userId': userCreated_obj.inserted_id, 'email': createdUser_dict["email"], 'token': token})
    return dumps({'userId': str(createdUser_dict["_id"]), 'email': createdUser_dict["email"], 'token': token})



def login(email, password): # working

    db= client.Share_It
    collection=db.users

    hasUser=''
    try:
        hasUser= collection.find_one({'email':email})
        # print("hasUser_obj",hasUser_obj)
        # hasUser=dumps(hasUser_obj)
        print("hasUser",hasUser)
    except Exception as e:
        return {"message": "Logging in failed. Please try again."}

    if (hasUser=='' or hasUser==None):
        error = http_error.HttpException("Logging in failed. Invalid credentials.", 401)
        return {"message": "Logging in failed. Invalid credentials."}

    isValidPassword = False
    try:
        print("isValidPassword1--->", isValidPassword)
        db_password=hasUser["password"]
        print("password",password)
        print("hasuser.password",db_password)
        isValidPassword=  bcrypt.check_password_hash(db_password,password) # 1st ar-> password from db , 2nd arg -> th passwo
        print("isValidPassword--->",isValidPassword)
    except Exception as e:
        print("error",e)
        error = http_error.HttpException("Logging in failed. Invalid credentials.",500)
        return {"message": "Logging in failed. Invalid credentials."}

    if (not isValidPassword):

        error = http_error.HttpException("Logging in failed. Invalid credentials.",401)
        return {"message": "Logging in failed. Invalid credentials."}

    token=''
    try:
        token= create_access_token(identity=str(hasUser['_id']))  # create jwt token
    except Exception as e:
        print(e)
        error = http_error.HttpException("Login failed. Please try again..", 500)
        return {"message": "Logging in failed. Please try again.."}

    return {'userId': str(hasUser["_id"]), 'email': hasUser["email"], 'token': token}
