from stellrent_response import json_response
from flask import Response
from pydantic import validate_call
import json

default_content_type = "application/json"

content_response_data = {
    "param1": "value1",
    "param2": "value2",
    "param3": "value3",
    "param4": "value4"
 }

def __test_basic_success_data_response(response:json_response.DataResponse):
    assert(response.response_status == 200)
    assert(response.response_data == content_response_data)
    assert(response.response_message == None)
    assert(response.response_details == None)
    response_obj = response.make_response()
    assert(response_obj.content_length is not None)
    assert(response_obj.content_length > 0)
    assert(response_obj.status_code == 200)
    assert(response_obj.content_type == default_content_type)
    assert(isinstance(response_obj, Response))

def test_response():
    success_content_resp = json_response.DataResponse(data=content_response_data)
    __test_basic_success_data_response(success_content_resp)
    response_obj = success_content_resp.make_response()
    response_data_dict = json.loads(response_obj.get_data())
    assert(len(content_response_data) == len(response_data_dict))
    assert(content_response_data == response_data_dict)