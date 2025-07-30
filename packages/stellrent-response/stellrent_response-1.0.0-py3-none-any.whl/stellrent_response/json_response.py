# -*- coding: utf-8 -*-
import logging
from pydantic import validate_call
from flask import Response
import json
from typing import Any, Optional

default_messages = {
    200: "Request executed successfully",
    201: "Created",
    204: None,
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Resource Not Found",
    405: "Method not allowed",
    500: "Internal Server Error"
}

class DefaultResponse():

    def __init__(self, logger: Optional[logging.Logger] = None):
        if logger and isinstance(logger, logging.Logger):
            self._logger = logger
        else:
            self._logger = logging.getLogger(self.__class__.__name__)
            if logger is not None: # A logger was provided but was invalid
                self._logger.warning(
                    f"Invalid logger type: {type(logger)}. Expected {logging.Logger}. "
                    f"Using default logger '{self._logger.name}'."
                )
        self.response_data: Optional[Any] = None
        self.response_status: int = 200
    
    @validate_call
    def make_response(self) -> Response:
        if self.response_status == 204:
            # HTTP 204 No Content responses must not include a message-body
            # or a Content-Type header.
            # Initialize with mimetype="" to ensure the content_type property is None
            # and to prevent a Content-Type header from being sent.
            response = Response(status=204, mimetype="")
            return response

        response = Response(
            content_type = "application/json",
            status = self.response_status
        )

        if self.response_data is not None:
            response.set_data(json.dumps(self.response_data))
        else:
            response_body = {}
            message = getattr(self, 'response_message', None)
            details = getattr(self, 'response_details', None)

            if message is not None:
                response_body["message"] = message
            if details is not None:
                response_body["details"] = details
            
            if response_body:
                response_body["status"] = self.response_status
                response.set_data(json.dumps(response_body))
            # If response_body is empty for an error status, provide a minimal default.
            elif self.response_status >= 400:
                fallback_message = default_messages.get(self.response_status, "Error")
                response.set_data(json.dumps({"message": fallback_message, "status": self.response_status}))
            # For non-error, non-204, non-data responses with no message/details,
            # an empty body (Content-Length: 0) is acceptable.
        return response
    
class DataResponse(DefaultResponse):
    def __init__(self, data: Any, logger: Optional[logging.Logger] = None):
        super().__init__(logger=logger)
        self.response_data = data
        self.response_message = None
        self.response_status = 200
        self.response_details = None
    
class ConfirmationResponse(DefaultResponse):
    def __init__(self, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(logger=logger)
        self.response_data = None
        self.response_message = default_messages[200]
        self.response_status = 200
        self.response_details = details
    
class CreateConfirmationResponse(DefaultResponse):
    def __init__(self, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(logger=logger)
        self.response_data = None
        self.response_message = default_messages[201]
        self.response_status = 201
        self.response_details = details
    
class NoDataResponse(DefaultResponse):
    def __init__(self, logger: Optional[logging.Logger] = None):
        super().__init__(logger=logger)
        self.response_data = None
        self.response_message = default_messages[204]
        self.response_status = 204
        self.response_details = None
    
class ErrorResponse(DefaultResponse):
    def __init__(self, status: int, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(logger=logger)
        self.response_data = None
        self.response_status = status
        self.response_message = default_messages.get(status)
        self.response_details = details

class BadRequest(ErrorResponse):
    def __init__(self, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(status=400, details=details, logger=logger)

class MethodNotAllowed(ErrorResponse):
    def __init__(self, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(status=405, details=details, logger=logger)

class ServerError(ErrorResponse):
    def __init__(self, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(status=500, details=details, logger=logger)

class Unauthorized(ErrorResponse):
    def __init__(self, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(status=401, details=details, logger=logger)

class Forbidden(ErrorResponse):
    def __init__(self, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(status=403, details=details, logger=logger)

class NotFound(ErrorResponse):
    def __init__(self, details: Optional[Any] = None, logger: Optional[logging.Logger] = None):
        super().__init__(status=404, details=details, logger=logger)
