from stellrent_response import json_response
from flask import Response

default_content_type = "application/json"

def __test_basic_not_found_response(response:json_response.BadRequest):
    assert(response.response_status == 204)
    assert(response.response_data == None)
    assert(response.response_message == None)
    assert(response.response_details == None)
    response_obj = response.make_response()
    assert(response_obj.content_length is None)
    # assert(response_obj.get_data() == None)
    assert(response_obj.status_code == 204)
    assert(response_obj.content_type == default_content_type)
    assert(isinstance(response_obj, Response))

def test_nocontent_response():
    no_content_response = json_response.NoDataResponse()
    __test_basic_not_found_response(no_content_response)
