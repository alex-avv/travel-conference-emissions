# pylint: disable = C0103, C0114, C0115, C0116
# type: ignore
from pytest import raises
from cities import City, CityCollection


def test_City_attributes_type():

    with raises(TypeError) as exception:
        City(9, 'France', 173, 48.8566101, 2.3514992)
    assert exception.match("Name should be given as a string")

    with raises(TypeError) as exception:
        City('Paris', 7.0, 173, 48.8566101, 2.3514992)
    assert exception.match("Country should be given as a string")

    with raises(TypeError) as exception:
        City('Paris', 'France', 173.0, 48.8566101, 2.3514992)
    assert exception.match("Number of attendees should be given as an integer")

    with raises(TypeError) as exception:
        City('Paris', 'France', 173, '48.8566101', 2.3514992)
    assert exception.match("Latitude should be given as a floating point "
                           "number")

    with raises(TypeError) as exception:
        City('Paris', 'France', 173, 48.8566101, 2)
    assert exception.match("Longitude should be given as a floating point "
                           "number")
    
def test_City_attributes_value():

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
        City('Paris', 'France', 173, 48.8566101, -181.0)
    assert str(exception.value) == ("Longitude should be between -180 and 180 "
                                    "degrees")
