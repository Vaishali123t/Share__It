from os import environ
from flask import Flask
from flask import current_app
from datetime import datetime, timedelta
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from routes.user_routes import users_blueprint
from routes.places_routes import places_blueprint
# from globals import login_manager
# from globals import client

app=Flask(__name__,static_url_path='',static_folder='uploads/images')
CORS(app)

jwt = JWTManager(app) # initialize JWTManager
app.config['JWT_SECRET_KEY'] = environ.get('JWT_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1) # define the life span of the token


app.register_blueprint(users_blueprint, url_prefix='/api/users')
app.register_blueprint(places_blueprint, url_prefix='/api/places')

@app.route("/uploads/images/<imgName>")
def serveImage(imgName):
    print("Serving images")
    return current_app.send_static_file(imgName)

app.run(host='0.0.0.0',debug=True)
# app.run(APP_URL)