# pylint: disable = C0114, C0115, C0116
from typing import Dict, List, Tuple


class City:
    def __init__(self, name: str, country: str, num_attendees: int,
                 lat: float, long: float):
        if not isinstance(name, str):
            raise TypeError("Name should be given as a string")
        if not isinstance(country, str):
            raise TypeError("Country should be given as a string")
        if not isinstance(num_attendees, int):
            raise TypeError("Number of attendees should be given as a integer")
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
        if long < -180.0 or long > 180.0:
            raise ValueError("Longitude should be between -180 and 180 "
                             "degrees")

        self.name = name
        self.country = country
        self.num_attendees = num_attendees
        self.lat = lat
        self.long = long

    def distance_to(self, other: 'City') -> float:
        raise NotImplementedError

    def co2_to(self, other: 'City') -> float:
        raise NotImplementedError


class CityCollection:
    ...

    def countries(self) -> List[str]:
        raise NotImplementedError

    def total_attendees(self) -> int:
        raise NotImplementedError

    def total_distance_travel_to(self, city: City) -> float:
        raise NotImplementedError

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
