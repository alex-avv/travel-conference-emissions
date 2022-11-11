# pylint: disable = C0114, C0115, C0116
from typing import Dict, List, Tuple
from math import pi, sqrt, sin, cos, asin


class City:
    def __init__(self, name: str, country: str, num_attendees: int,
                 lat: float, long: float):
        if not isinstance(name, str):
            raise TypeError("Name should be given as a string")
        if not isinstance(country, str):
            raise TypeError("Country should be given as a string")
        if not isinstance(num_attendees, int):
            raise TypeError("Number of attendees should be given as an "
                            "integer")
        if not isinstance(lat, float):
            raise TypeError("Latitude should be given as a floating point "
                            "number")
        if not isinstance(long, float):
            raise TypeError("Longitude should be given as a floating point "
                            "number")

        if name[0].islower():
            raise ValueError("First letter in name should be upper case")
        if country[0].islower():
            raise ValueError("First letter in country should be upper case")
        if num_attendees < 0:
            raise ValueError("Number of attendees should be a positive "
                             "integer")
        if lat < -90.0 or lat > 90.0:
            raise ValueError("Latitude should be between -90 and 90 degrees")
        if long <= -180.0 or long > 180.0:
            raise ValueError("Longitude should be between -180 and 180 "
                             "degrees")

        self.name = name
        self.country = country
        self.num_attendees = num_attendees
        self.lat = lat
        self.long = long
        self.lat_rad = lat * pi / 180
        self.long_rad = long * pi / 180

    def distance_to(self, other: 'City') -> float:
        earth_r = 6371
        dis = (2 * earth_r *
               asin(sqrt(((sin((self.lat_rad - other.lat_rad) / 2)) ** 2)
                         + cos(other.lat_rad) * cos(self.lat_rad) *
                         ((sin((self.long_rad - other.long_rad) / 2)) ** 2))))
        return dis

    def co2_to(self, other: 'City') -> float:
        dis = self.distance_to(other)
        if dis <= 1000.0:
            return dis * 200 * self.num_attendees
        if dis <= 8000.0:
            return dis * 250 * self.num_attendees
        return dis * 300 * self.num_attendees


class CityCollection:
    def __init__(self, cities: List[City]):
        if not isinstance(cities, list):
            raise TypeError("Cities should be given as a list of City objects")
        if not all([isinstance(city, City) for city in cities]):
            raise TypeError("Cities should be given as a list of only City "
                            "objects")

        self.cities = cities

    def countries(self) -> List[str]:
        return sorted(list(set([city.country for city in self.cities])))

    def total_attendees(self) -> int:
        return sum([city.num_attendees for city in self.cities])

    def total_distance_travel_to(self, city: City) -> float:
        host_city = city
        return sum([city.distance_to(host_city) * city.num_attendees
                    for city in self.cities if city != host_city])

    def travel_by_country(self, city: City) -> Dict[str, float]:
        raise NotImplementedError

    def total_co2(self, city: City) -> float:
        raise NotImplementedError

    def co2_by_country(self, city: City) -> Dict[str, float]:
        raise NotImplementedError

    def summary(self, city: City):
        raise NotImplementedError

    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        raise NotImplementedError

    def plot_top_emitters(self, city: City, n: int, save: bool):
        raise NotImplementedError
