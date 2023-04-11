import requests
from flask import Blueprint, request


from controllers import users_controllers as usersControllers
# from  middlewares import file_upload as fileUpload
# from  middlewares import check_auth as checkAuth

users_blueprint=Blueprint('users_blueprint',__name__)

# find a user by uid
@users_blueprint.route('/<uid>',methods=['GET'])
def getUserByPid(uid):
    ans= usersControllers.getUserById(uid)
    return ans

#  find all users
@users_blueprint.route('/',methods=['GET'])
async def getUsers():
    return await usersControllers.getAllUsers()
    # return {"users":[{"id": "642cccc9ab303d14fc5474ff", "places": [], "name": "testing1", "email": "testing1@g.com", "image": "https://live.staticflickr.com/7631/26849088292_36fc52ee90_b.jpg", "password": "testing1"}]}

# signup
@users_blueprint.route('/signup',methods=['POST'])
async def signUp():
    file=request.files['image']
    name= request.form.get('name')
    email= request.form.get('email')
    password= request.form.get('password')
    return await usersControllers.signUp(name, email, password,file)

# login
@users_blueprint.route('/login',methods=['POST'])
def login():
    user= request.get_json()
    email= user['email']
    password=user['password']
    return usersControllers.login(email, password)


