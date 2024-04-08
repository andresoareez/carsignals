import os
import json
import datetime
import pytest
import random
import string
from transformers.mercedes_transformer import transform_mercedes 
from transformers.bmw_transformer import transform_bmw 
from utils.logger import get_logger
from tests.conftest.conftests import mercedes_sample_data, bmw_sample_data

logger = get_logger(__name__)
        
def test_sample_data_mercedes(mercedes_sample_data):
    #Test with a valid datas
    
    
    mock_data = mercedes_sample_data
    transformed_data = transform_mercedes(mock_data)
    
    assert 'timestamp' in transformed_data
    assert 'vin' in transformed_data
    assert 'fleet_id' in transformed_data
    assert 'uuid' in transformed_data
    assert 'eco_score_acceleration' in transformed_data
    assert 'anti_theft_alarm_triggered' not in transformed_data

    assert transformed_data['timestamp'] == '2020-06-22 19:24:09+00:00'
    assert transformed_data['vin'] == 'WDD2130481A123456'        

def test_missing_data_mercedes(mercedes_sample_data):
    # Test with missing 'data' key in the mockdata
    mock_data = mercedes_sample_data
    mock_data['vin'] = None
    mock_data['timestamp'] = ""
    transformed_data = transform_mercedes(mock_data)

    assert 'timestamp' not in transformed_data
    assert transformed_data['vin'] == None
    assert transformed_data['fleet_id'] == None  
    assert  transformed_data['uuid'] == None  


def test_transform_mercedes_missing_signals(mercedes_sample_data):
    # Test with missing 'signals' key in the mock data
    mock_data = mercedes_sample_data
    mock_data['data']['signals'] = ""
    transformed_data = transform_mercedes(mock_data)
    assert 'signals' not in transformed_data 
    
    
def test_transform_mercedes_invalid_timestamp(mercedes_sample_data):
    # Test with an invalid 'timestamp' value (string instead of int/float)
    mock_data = mercedes_sample_data
    mock_data["timestamp"] = "1592853849159"
    transformed_data = transform_mercedes(mock_data)

    assert 'timestamp' not in transformed_data
    
# def test_transform_bmw(bmw_sample_data):
#     mock_data = bmw_sample_data
#     vin = 'WB' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))
#     transformed_data = transform_bmw(mock_data, vin)

    
    
#     assert 'latitude' in transformed_data
#     assert 'longitude' in transformed_data
#     assert 'altitude' in transformed_data
#     assert 'heading' in transformed_data
#     assert 'vin' in transformed_data

