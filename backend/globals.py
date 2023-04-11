'''
 These are global variables which will have to import in various modules
'''

# from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from pymongo import MongoClient
from os import environ

# login manager setup
# login_manager=LoginManager()

# Database setup
db_user= environ.get('DB_USER')
# print(db_user)
db_password= environ.get('DB_PASSWORD')
db_url=f'mongodb+srv://{db_user}:{db_password}@cluster0.fgal3tb.mongodb.net/?retryWrites=true&w=majority'
# print(db_url)
client= MongoClient(db_url)

# for encryption
bcrypt=Bcrypt()

