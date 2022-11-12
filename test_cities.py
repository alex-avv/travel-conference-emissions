# pylint: disable = C0103, C0114, C0115, C0116
# type: ignore
import json
from pytest import mark, raises
from cities import City, CityCollection

with open('test_fixtures.json', 'r', encoding="utf-8") as json_test_fixtures:
    dict_test_fixtures = json.load(json_test_fixtures)


@mark.parametrize('test_name', dict_test_fixtures['City_properties_type'])
def test_City_properties_type(test_name):
    buffer = list(test_name.values())[0]
    city_input = buffer['properties']
    expected_err_message = buffer['expected_err_message']

    with raises(TypeError) as exception:
        City(*city_input)
    assert str(exception.value) == expected_err_message


@mark.parametrize('test_name', dict_test_fixtures['City_properties_value'])
def test_City_properties_value(test_name):
    buffer = list(test_name.values())[0]
    city_input = buffer['properties']
    expected_err_message = buffer['expected_err_message']

    with raises(ValueError) as exception:
        City(*city_input)
    assert str(exception.value) == expected_err_message


@mark.parametrize('test_name', dict_test_fixtures['distance_to'])
def test_distance_to(test_name):
    buffer = list(test_name.values())[0]
    host_city_input = buffer['properties_host_city']
    visitor_city_input = buffer['properties_visitor_city']
    expected_value = buffer['expected_value']

    host_city, visitor_city = City(*host_city_input), City(*visitor_city_input)
    distance = visitor_city.distance_to(host_city)
    assert distance == expected_value


@mark.parametrize('test_name', dict_test_fixtures['co2_to'])
def test_co2_to(test_name):
    buffer = list(test_name.values())[0]
    host_city_input = buffer['properties_host_city']
    visitor_city_input = buffer['properties_visitor_city']
    expected_value = buffer['expected_value']

    host_city, visitor_city = City(*host_city_input), City(*visitor_city_input)
    co2 = visitor_city.co2_to(host_city)
    assert co2 == expected_value

def test_read_attendees_file():
    raise NotImplementedError
