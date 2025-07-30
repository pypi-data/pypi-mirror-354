from stellrent_response import json_response
from flask import Response
import json

detailed_error_message = "A detailed error message"
custom_message = "A custom Bad Request message"
default_message = "Bad Request"
default_content_type = "application/json"

def __test_basic_bad_response(response:json_response.BadRequest):
    assert(response.response_status == 400)
    assert(response.response_data == None)
    assert(response.response_message is not None)
    response_obj = response.make_response()
    assert(response_obj.status_code == 400)
    assert(response_obj.content_type == default_content_type)
    assert(isinstance(response_obj, Response))

def test_response():
    bad_request_response = json_response.BadRequest()
    __test_basic_bad_response(bad_request_response)
    assert(bad_request_response.response_details == None)
    bad_request_response_obj = bad_request_response.make_response()
    response_data_dict = json.loads(bad_request_response_obj.get_data())
    assert(len(response_data_dict) == 2)
    assert(response_data_dict['message'] == json_response.default_messages[400])
    assert(response_data_dict['status'] == 400)

def test_response_with_details():
    bad_request_response = json_response.BadRequest(details=detailed_error_message)
    __test_basic_bad_response(bad_request_response)
    assert(bad_request_response.response_details is not None)
    response_obj = bad_request_response.make_response()
    response_data_dict = json.loads(response_obj.get_data())
    assert(len(response_data_dict) == 3)
    assert(response_data_dict['details'] == detailed_error_message)
    assert(response_data_dict['message'] == json_response.default_messages[400])
    assert(response_data_dict['status'] == 400)

def test_response_with_custom_message():
    bad_request_response = json_response.BadRequest()
    bad_request_response.response_message = custom_message
    __test_basic_bad_response(bad_request_response)
    assert(bad_request_response.response_details is None)
    response_obj = bad_request_response.make_response()
    response_data_dict = json.loads(response_obj.get_data())
    assert(len(response_data_dict) == 2)
    assert(response_data_dict['message'] == custom_message)
    assert(response_data_dict['status'] == 400)

def test_response_with_details_and_custom_message():
    bad_request_response = json_response.BadRequest(detailed_error_message)
    bad_request_response.response_message = custom_message
    __test_basic_bad_response(bad_request_response)
    assert(bad_request_response.response_details is not None)
    response_obj = bad_request_response.make_response()
    response_data_dict = json.loads(response_obj.get_data())
    assert(len(response_data_dict) == 3)
    assert(response_data_dict['message'] == custom_message)
    assert(response_data_dict['details'] == detailed_error_message)
    assert(response_data_dict['status'] == 400)
