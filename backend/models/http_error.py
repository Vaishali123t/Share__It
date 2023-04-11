class HttpException(Exception):

    def __init__(self, message, errorCode):
        self.message= message
        self.errorCode= errorCode
        a=super().__init__(message)
        print("error-->",a)
        return a
