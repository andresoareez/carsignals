import json
import base64

from ..aws.lambdas.vin_kafka_sink_c1 import lambda_handler
from .conftests.conftests import mock_right_vin_validation, mock_wrong_vin_validation

def test_valid_vin(mock_right_vin_validation):
    event = {
        'Records': [
            {
                'kinesis': {
                    'data': base64.b64encode(base64.b64encode(json.dumps(mock_right_vin_validation).encode('utf-8'))).decode('utf-8')
                }
            }
        ]
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 200
    assert 'vin' in json.loads(result['body'])

def test_invalid_vin(mock_wrong_vin_validation):
    event = {
        'Records': [
            {
                'kinesis': {
                    'data': base64.b64encode(base64.b64encode(json.dumps(mock_wrong_vin_validation).encode('utf-8'))).decode('utf-8')
                }
            }
        ]
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 400
    assert result['body'] == "The VIN number is not valid"
