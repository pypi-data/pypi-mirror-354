from stellrent_response import json_response
from flask import Response

default_content_type = "application/json"

def test_nocontent_response():
    no_content_response = json_response.NoDataResponse()
    assert(no_content_response.response_status == 204)
    assert(no_content_response.response_data is None)
    assert(no_content_response.response_message == None)
    assert(no_content_response.response_details == None)
    response_obj = no_content_response.make_response()
    assert(response_obj.content_length is None)
    assert(response_obj.get_data() == b'') # Flask returns an empty bytes object for 204
    assert(response_obj.status_code == 204)
    assert(response_obj.content_type == "") # For mimetype="", content_type becomes ""
    assert(isinstance(response_obj, Response))
