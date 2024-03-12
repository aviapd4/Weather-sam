import json
from unittest.mock import MagicMock, patch
import pytest
from add_function import create_handler, delete_handler
from delete_function import  delete_handler


@pytest.fixture()
def dynamodb_client():
    with patch('your_lambda_file.boto3.client') as mock_client:
        yield mock_client('dynamodb')
        

@pytest.fixture()
def event():
    return {
        'id': '123',
        'Weather': 'Sunny',
        'token': 'allowme'
    }


def test_create_handler_successful_update(dynamodb_client, event):
    dynamodb_client.put_item.return_value = {}

    response = create_handler(event, None)

    assert response['statusCode'] == 200
    assert response['body'] == 'Successfully inserted data!'


def test_create_handler_missing_authorization_attribute(event):
    del event['token']  # Simulating missing token

    response = create_handler(event, None)

    assert response['statusCode'] == 401
    assert response['body'] == 'Missing authorisation attributes.'


def test_create_handler_unauthorized_operation(event):
    event['token'] = 'invalidtoken'  # Simulating unauthorized token

    response = create_handler(event, None)

    assert response['statusCode'] == 401
    assert response['body'] == 'You are not authorized to perform this task.'


def test_create_handler_missing_required_attributes(event):
    del event['Weather']  # Simulating missing Weather attribute

    response = create_handler(event, None)

    assert response['statusCode'] == 400
    assert response['body'] == 'Missing required attributes.'


def test_create_handler_extra_attributes(event):
    event['extra'] = 'attribute'  # Simulating extra attribute

    response = create_handler(event, None)

    assert response['statusCode'] == 400
    assert response['body'] == 'Extra attributes are not allowed.'


def test_delete_handler_successful_deletion(dynamodb_client, event):
    dynamodb_client.delete_item.return_value = {}

    response = delete_handler(event, None)

    assert response['statusCode'] == 200
    assert response['body'] == 'Item deleted successfully'


def test_delete_handler_missing_authorization_attribute(event):
    del event['token']  # Simulating missing token

    response = delete_handler(event, None)

    assert response['statusCode'] == 401
    assert response['body'] == 'Missing authorisation attributes.'


def test_delete_handler_unauthorized_operation(event):
    event['token'] = 'invalidtoken'  # Simulating unauthorized token

    response = delete_handler(event, None)

    assert response['statusCode'] == 401
    assert response['body'] == 'You are not authorized to perform this task.'


def test_delete_handler_missing_id_attribute(event):
    del event['id']  # Simulating missing id attribute

    response = delete_handler(event, None)

    assert response['statusCode'] == 400
    assert response['body'] == 'Missing required attribute: id'
