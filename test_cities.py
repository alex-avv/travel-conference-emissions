# pylint: disable = C0103, C0114, C0115, C0116, W0621
# type: ignore
from pathlib import Path
import json
from pytest import mark, raises
from cities import City, CityCollection
from utils import read_attendees_file

with open('fixtures.json', 'r', encoding="utf-8") as json_test_fixtures:
    dict_test_fixtures = json.load(json_test_fixtures)

# Test to check data sample file is in the same folder
sample_file_path = Path("./data_sample.csv")
if not sample_file_path.is_file():
    raise FileNotFoundError("'data_sample.csv' file required for "
                            "CityCollection's methods tests must be in the "
                            f"same directory as {Path(__file__).name}")


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


def test_read_attendees_file_type():
    file_path = 9474
    expected_err_message = ("File path should be given as a pathlib.Path "
                            "object or a string")

    with raises(TypeError) as exception:
        read_attendees_file(file_path)
    assert str(exception.value) == expected_err_message


def create_equivalent_city_collection():
    host_city = City('Host City', 'Host Country', 10, 0.0, 0.0)
    host_city_equivalent = City('Host City', 'Host Country', 10, 0.0, 0.0)
    city_a = City('City A', 'Country A', 5, -8.993216059187306, 0.0)
    city_b = City('City B', 'Country E', 2, 71.94572847349845, 0.0)
    city_c = City('City C', 'Country D', 5, 0.0, -89.93216059187306)
    city_d = City('City D', 'Host Country', 5, 0.0,  8.993216059187306)
    city_e = City('City E', 'Country C', 1, 47.0, -13.0)
    city_f = City('City F', 'Country B', 1, 25.0, -113.0)
    city_g = City('City G', 'Country C', 2, 41.288795, -5.222789)
    city_h = City('City H', 'Country F', 2, -71.94572847349845, 0.0)
    empty_city = City('Empty City', 'Empty Country', 0, -60.0, 130.0)

    city_objects_list = [host_city_equivalent, city_a, city_b, city_c, city_d,
                         city_e, city_f, city_g, city_h, empty_city]
    return CityCollection(city_objects_list), host_city


city_collection = read_attendees_file(sample_file_path)
_, host_city = create_equivalent_city_collection()


@mark.parametrize('city_collection', [city_collection])
def test_CityCollection_properties_type(city_collection):
    expected_err_message = "Cities should be given as a list of City objects"
    with raises(TypeError) as exception:
        CityCollection(tuple(city_collection.cities))
    assert str(exception.value) == expected_err_message

    expected_err_message = ("Cities list is empty. It should have at least "
                            "one element")
    with raises(ValueError) as exception:
        CityCollection([])
    assert str(exception.value) == expected_err_message

    expected_err_message = ("Cities should be given as a list of only City "
                            "objects")
    with raises(TypeError) as exception:
        CityCollection(city_collection.cities + ['foo'])
    assert str(exception.value) == expected_err_message
