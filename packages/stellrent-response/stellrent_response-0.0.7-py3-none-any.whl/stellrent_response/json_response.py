# -*- coding: utf-8 -*-
import inspect
import logging
from pydantic import validate_call
from flask import Response
import json

default_messages = {
    200: "Request executed successfully",
    201: "Created",
    204: None,
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Resource Not Found",
    405: "Method not alowed",
    500: "Internal Server Error"
}

class DefaultResponse():

    __logger = logging.getLogger()

    def __init__(self, logger=None):
        if logger is None:
            self.__logger = logging.getLogger()
        else:
            if isinstance(logger, logging.getLogger()):
                self.__logger = logger
            else:
                self.__logger = logging.getLogger()
                self.__logger.warning("Invalid logger: " + type(logger) + ". Expected logger type: " + type(self.logger))
        self.response_data = None
        self.response_status = 200
    
    @validate_call
    def make_response(self, data:str = None, details:str = None) -> Response:
        # for i in inspect.getmembers(self):
        #     if i[0].startswith('response_') and not inspect.ismethod(i[0]):
        #         if i[1] is not None:
        #             body_response[i[0].replace('response_', "")] = i[1]
        
        response = Response(
            content_type = "application/json",
            status = self.response_status
        )

        if self.response_data:
            response.set_data(json.dumps(self.response_data))
        else:
            # aditional response informations (except data)
            response_body = {}
            if self.response_message:
                response_body["message"] = self.response_message
            if self.response_details:
                response_body["details"] = self.response_details
            
            if len(response_body) > 0:
                response_body["status"] = self.response_status
                response.set_data(json.dumps(response_body))
        return response
    
class DataResponse(DefaultResponse):
    def __init__(self, data:str):
        DefaultResponse.__init__(self)
        self.response_data = data
        self.response_message = None
        self.response_status = 200
        self.response_details = None

    def make_response(self):
        return super().make_response()
    
class ConfirmationResponse(DefaultResponse):
    def __init__(self, details):
        DefaultResponse.__init__(self)
        self.response_data = None
        self.response_message = default_messages[200]
        self.response_status = 200
        self.response_details = details

    def make_response(self):
        return super().make_response()
    
class CreateConfirmationResponse(DefaultResponse):
    def __init__(self, details):
        DefaultResponse.__init__(self)
        self.response_data = None
        self.response_message = default_messages[201]
        self.response_status = 201
        self.response_details = details

    def make_response(self):
        return super().make_response()
    
class NoDataResponse(DefaultResponse):
    def __init__(self):
        DefaultResponse.__init__(self)
        self.response_data = None
        self.response_message = default_messages[204]
        self.response_status = 204
        self.response_details = None

    def make_response(self):
        return super().make_response()

    
class ErrorResponse(DefaultResponse):

    def __init__(self):
        DefaultResponse.__init__(self)
        self.response_data = None
        self.response_message = None
        self.response_status = None
        self.response_details = None

class BadRequest(ErrorResponse):

    def __init__(self, details=None):
        ErrorResponse.__init__(self)
        self.response_data = None
        self.response_message = default_messages[400]
        self.response_status = 400
        self.response_details = details


class MethodNotAllowed(ErrorResponse):

    def __init__(self, details=None):
        self.response_data = None
        self.response_status = 405
        self.response_message = default_messages[405]
        self.response_details = details

class ServerError(ErrorResponse):

    def __init__(self, details=None):
        self.response_data = None
        self.response_status = 500
        self.response_message = default_messages[500]
        self.response_details = details

class Unauthorized(ErrorResponse):

    def __init__(self, details=None):
        self.response_data = None
        self.response_status = 401
        self.response_message = default_messages[401]
        self.response_details = details

class Forbidden(ErrorResponse):

    def __init__(self, details=None):
        self.response_data = None
        self.response_status = 403
        self.response_message = default_messages[403]
        self.response_details = details

class NotFound(ErrorResponse):

    def __init__(self, details=None):
        self.response_data = None
        self.response_status = 404
        self.response_message = default_messages[404]
        self.response_details = details
