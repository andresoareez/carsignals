import pytest


@pytest.fixture
def mock_right_vin_validation():
    return {
    "messageId": "12876bd0-c211-49c3-ade1-ee755cfc7525",
    "vin": "WDD2130481A123456",
    "timestamp": 1592853849159,
    "messageType": "vehiclesignal",
    "version": "1",
    "serviceId": "1001",
    "sendingBehaviour": "ON_INTERVAL_120_SEC",
        "data": {    
        "signals": [
            {
                "name": "Driving.EcoScore.Acceleration",
                "timestamp": 1592853849159,
                "value": "true",
                "type": "boolean"
            }
            ]
        }
    }


def mock_wrong_vin_validation():
    return {
    "messageId": "12876bd0-c211-49c3-ade1-ee755cfc7525",
    "vin": "INVALIDVIN123",
    "timestamp": 1592853849159,
    "messageType": "vehiclesignal",
    "version": "1",
    "serviceId": "1001",
    "sendingBehaviour": "ON_INTERVAL_120_SEC",
        "data": {    
        "signals": [
            {
                "name": "Driving.EcoScore.Acceleration",
                "timestamp": 1592853849159,
                "value": "true",
                "type": "boolean"
            }
            ]
        }
    }