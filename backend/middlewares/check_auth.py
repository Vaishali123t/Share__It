
# jwt = require("jsonwebtoken");

from ..models import http_error
#
# module.exports = (req, res, next) = > {
# if (req.method === "OPTIONS")
#
# return next();

def authentication(token):
    try:
        # token = req.headers.authorization.split(" ")[1] # Authorization: 'BEARER TOKEN'
        if (not token):
            raise http_error.HttpException("Authentication failed!",404)

        decodedToken = jwt.verify(token, process.env.JWT_KEY)
        userData = {'userId': decodedToken.userId}
        
    except Exception as e:
        error = http_error.HttpException("Authentication failed!", 403)
        return next(error)