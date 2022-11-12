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


def test_City_properties_value():

    with raises(ValueError) as exception:
        City('paris', 'France', 173, 48.8566101, 2.3514992)
    assert str(exception.value) == ("First letter in name should be upper "
                                    "case")

    with raises(ValueError) as exception:
        City('Paris', 'france', 173, 48.8566101, 2.3514992)
    assert str(exception.value) == ("First letter in country should be upper "
                                    "case")

    with raises(ValueError) as exception:
        City('Paris', 'France', -173, 48.8566101, 2.3514992)
    assert str(exception.value) == ("Number of attendees should be a positive "
                                    "integer")

    with raises(ValueError) as exception:
        City('Paris', 'France', 173, 91.0, 2.3514992)
    assert str(exception.value) == ("Latitude should be between -90 and 90 "
                                    "degrees")

    with raises(ValueError) as exception:
        City('Paris', 'France', 173, 48.8566101, -180.0)
    assert str(exception.value) == ("Longitude should be between -180 and 180 "
                                    "degrees")
