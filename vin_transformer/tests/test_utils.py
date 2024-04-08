import pytest
from utils.utils import cast_value, get_fleet_and_uuid

def test_cast_value():
    assert cast_value("123", "integer") == 123
    assert cast_value("1.65", "double") == 1.65
    assert cast_value("true", "boolean") is True
    assert cast_value("false", "boolean") is False
    assert cast_value("2023-11-14", "datetime") == "2023-11-14"
    assert cast_value("test", "string") == "test"
    
    
def test_get_fleet_and_uuid():
    vehicle_to_fleet = {"testvehicle1": "fleet1"}
    fleet_to_uuid = {"fleet1": "uuid1"}

    result = get_fleet_and_uuid("testvehicle1", vehicle_to_fleet, fleet_to_uuid)

    assert result == ("fleet1", "uuid1")