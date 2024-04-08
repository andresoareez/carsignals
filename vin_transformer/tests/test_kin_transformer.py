import pytest
from aws.lambdas.kinesis_transformer_lambda import lambda_handler
from .conftest.conftests import sample_data_mercedes_kinesis_event, mercedes_sample_data
import json
import base64

def test_lambda_handler_mercedes_sample(sample_data_mercedes_kinesis_event, mercedes_sample_data):
    mock_data = sample_data_mercedes_kinesis_event
    response = lambda_handler(mock_data, None)
    
    record_check = mercedes_sample_data
    source_record = record_check['messageId']
    
    assert 'records' in response
    assert len(response['records']) == 1
    
    record_output = response['records'][0]
    data_try = record_output['data']
    decoded_data = base64.b64decode(data_try.encode('utf-8'))
    decoded_data2 = decoded_data.rstrip(b'\n')
    json_data = decoded_data2.decode('utf-8')
    
    decoded_data = json.loads(json_data)
    assert 'window_rear_left_is_open' in decoded_data
    assert decoded_data['timestamp'] == '2020-06-22 19:24:09+00:00'
    
    assert record_output['recordId'] == source_record
    
    
    
