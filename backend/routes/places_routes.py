
import requests
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
# from flask_login import login_required

places_blueprint=Blueprint('places_blueprint',__name__)

from controllers import places_controllers as placesControllers


#  get a specific place by id
@places_blueprint.route('/<pid>',methods=['GET'])
def getPlaceBydPid(pid):
    return placesControllers.getPlaceById(pid)

# retrieve list of all places for a given uid
@places_blueprint.route('/user/<uid>',methods=['GET'])
async def getPlacesByUid(uid):
    return await placesControllers.getPlacesByUserId(uid)

# add a place given the details post authetication
@places_blueprint.route('/',methods=['POST'])
@jwt_required(optional=True)
async def addPlace():
    print("createPlace")
    # newplace= request.get_json()
    print('request.files',request.files['image'])
    print('request.form', request.form)
    file= request.files['image']
    title= request.form.get('title')
    description= request.form.get('description')
    address= request.form.get('address')

    current_user = get_jwt_identity()

    return await placesControllers.createPlace(current_user,title, description, address,file)


# update a place given the details post authetication

@places_blueprint.route('/<pid>',methods=['PATCH'])
@jwt_required(optional=True)
async def updatePlace(pid):
    # Get the identity of the current user
    current_user = get_jwt_identity()
    placesParamas = request.get_json()
    # userdata=request.use
    description=placesParamas['description']
    title=placesParamas['title']
    return await placesControllers.editPlaceById(pid,title,description,current_user)



# delete a place given the details post authetication
@places_blueprint.route('/<pid>',methods=['DELETE'])
@jwt_required(optional=True)
async def deletePlace(pid):
    return await placesControllers.deletePlaceById(pid)


