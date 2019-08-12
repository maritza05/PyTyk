#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `pytyk` package."""
from unittest.mock import Mock, patch
from nose.tools import assert_true, assert_is_instance, assert_equals, assert_raises, raises

import json

from pytyk.services import Tyk
from pytyk.tyk_exceptions import AuthorizationError, InvalidTykInstance, InvalidPolicy, InvalidTykOperation, TykInternalError


@patch('pytyk.services.requests.post')
def test_create_developer_with_valid_credentials(mock_get):
    result = {
        "Status": "OK",
        "Message": "5d4dc6ec0fe7814a21723022",
        "Meta": None
    }
    mock_get.return_value = Mock(ok=True)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = result
    tyk_client = Tyk(host='https://tyk.example.com', auth='valid_auth')
    response = tyk_client.create_developer('test@email.com', 'mypass', 'testorgid')
    assert_is_instance(response, str)

@raises(AuthorizationError)  
@patch('pytyk.services.requests.post')
def test_create_developer_with_invalid_credentials(mock_get):
    result = {
        "Status": "Error",
        "Message": "Not authorised",
        "Meta": None
    }
    mock_get.return_value.status_code = 401
    mock_get.return_value.json.return_value = result
    tyk_client = Tyk(host='https://tyk.example.com', auth='invalid_auth')
    response = tyk_client.create_developer('test@email.com', 'mypass', 'testorgid')

@raises(InvalidTykInstance)
@patch('pytyk.services.requests.post')
def test_create_developer_with_invalid_credentials(mock_get):
    mock_get.side_effect = ConnectionError()
    tyk_client = Tyk(host='InvalidTykHost', auth='invalid_auth')
    response = tyk_client.create_developer('test@email.com', 'mypass', 'testorgid')

@patch('pytyk.services.requests.post')
def test_create_developer_with_invalid_fields(mock_get):
    result = {
        "Status": "Error",
        "Message": "Developer object validation failed.",
        "Meta": None,
        "Errors": [
            "password: String length must be greater than or equal to 6"
        ]
    }
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = result
    tyk_client = Tyk(host='https://tyk.example.com', auth='valid_auth')
    response = tyk_client.create_developer('test@email.com', '', 'testorgid')
    assert_is_instance(response, str)

@patch('pytyk.services.requests.post')
def test_create_key_for_developer_with_valid_data(mock_get):
    result = {
        "Status": "OK",
        "Message": "5d518b530fe7814a21723026",
        "Meta": None
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = result
    tyk_client = Tyk(host='https://tyk.example.com', auth='valid_auth')
    response = tyk_client.create_key_for_developer('valid_dev_id', 'valid_policy')
    assert_is_instance(response, str)

@raises(InvalidTykOperation)
@patch('pytyk.services.requests.post')
def test_create_key_request_with_invalid_policy(mock_get):
    result = {
        "Status": "Error",
        "Message": "No policy found!",
        "Meta": None
    }
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = result
    tyk_client = Tyk(host='https://tyk.example.com', auth='valid_auth')
    response = tyk_client.create_key_for_developer('valid_dev_id', 'invalid_policy')
    assert_is_instance(response, str)

@patch('pytyk.services.requests.put')
def test_approve_key_with_a_valid_key(mock_get):
    result = {
        "RawKey": "5d0ec9930fe7815a7696d1f4b9d8c0a30dc844a4aa88ac2fdc4eda16",
        "Password": ""
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = result
    tyk_client = Tyk(host='https://tyk.example.com', auth='valid_auth')
    key = tyk_client.approve_key('valid_key')
    assert_equals(result['RawKey'], key)

@patch('pytyk.services.requests.put')
def test_approve_key_with_a_valid_key(mock_get):
    result = {
        "RawKey": "5d0ec9930fe7815a7696d1f4b9d8c0a30dc844a4aa88ac2fdc4eda16",
        "Password": ""
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = result
    tyk_client = Tyk(host='https://tyk.example.com', auth='valid_auth')
    key = tyk_client.approve_key('valid_key')
    assert_equals(result['RawKey'], key)

@raises(InvalidTykOperation)
@patch('pytyk.services.requests.put')
def test_approve_key_with_an_already_approved_key(mock_get):
    result = {
        "Status": "Error",
        "Message": "Key request has already been processed.",
        "Meta": None
    }
    mock_get.return_value.status_code = 400
    mock_get.return_value.json.return_value = result
    tyk_client = Tyk(host='https://tyk.example.com', auth='valid_auth')
    key = tyk_client.approve_key('invalid_key')

@raises(TykInternalError)
@patch('pytyk.services.requests.put')
def test_approve_key_with_invalid_key(mock_get):
    mock_get.return_value.status_code = 500
    tyk_client = Tyk(host='https://tyk.example.com', auth='valid_auth')
    key = tyk_client.approve_key('invalid_key')









