class APIException(Exception):
   pass

class StatusCodeException(APIException):
   def __init__(self, message, status_code, response_text):
       super().__init__(message)
       self.status_code = status_code
       self.response_text = response_text
       