# pylint: disable = C0103, C0114, C0115, C0116
from typing import Dict, List, Tuple
from math import pi, sqrt, sin, cos, asin
import matplotlib.pyplot as plt


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

        numbers = [str(num) for num in range(10)]

        if any([num in name[0] for num in numbers]):
            raise ValueError("First letter in name should be non-number")
        # Automatically capitalising first letter of name
        if name[0].islower():
            name = name[0].upper() + name[1:]

        if any([num in country[0] for num in numbers]):
            raise ValueError("First letter in country should be non-number")
        # Automatically capitalising first letter of country
        if country[0].islower():
            country = country[0].upper() + country[1:]

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
        if not cities:
            raise ValueError("Cities list is empty. It should have at least "
                             "one element")
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
                    for city in self.cities if city.name != host_city.name])

    def travel_by_country(self, city: City) -> Dict[str, float]:
        host_city = city
        return {country: sum([city.distance_to(host_city) * city.num_attendees
                              for city in self.cities
                              if city.name != host_city.name
                              and city.country == country
                              ])
                for country in self.countries()}

    def total_co2(self, city: City) -> float:
        host_city = city
        return sum([city.co2_to(host_city) for city in self.cities
                    if city.name != host_city.name])

    def co2_by_country(self, city: City) -> Dict[str, float]:
        host_city = city
        return {country: sum([city.co2_to(host_city) for city in self.cities
                              if city.name != host_city.name
                              and city.country == country
                              ])
                for country in self.countries()}

    def summary(self, city: City):
        host_city = city
        cities_not_host_not_empty = [city for city in self.cities
                                     if city.name != host_city.name
                                     and city.num_attendees > 0]
        total_cities_not_host_not_empty = len(cities_not_host_not_empty)
        total_attendees_not_host = sum([city.num_attendees
                                        for city in cities_not_host_not_empty])

        print(f"Host city: {host_city.name} ({host_city.country})\n"
              f"Total CO2: {round(self.total_co2(host_city) / 1000)} tonnes\n"
              f"Total attendees travelling to {host_city.name} "
              f"from {total_cities_not_host_not_empty} different cities: "
              f"{total_attendees_not_host}")

    def sorted_by_emissions(self) -> List[Tuple[str, float]]:
        return sorted([(host_city.name, self.total_co2(host_city))
                       for host_city in self.cities],
                      key=lambda tupl: tupl[1])

    def plot_top_emitters(self, city: City, n: int = 10, save: bool = False):
        host_city = city
        dict_co2_by_country = self.co2_by_country(host_city)

        if not isinstance(n, int):
            raise TypeError("Chosen top emitters number must be given as an "
                            "integer")
        if n < 1:
            raise ValueError(f"Chosen top emitters number ({n}) must be 1 or "
                              "larger")
        if n > 15:
            raise ValueError(f"Chosen top emitters number ({n}) is too large. "
                             "For a clear plot, set it lower than 15")
        if n > len(dict_co2_by_country):
            raise ValueError(f"Chosen top emitters number ({n}) is larger "
                             "than the available number of countries "
                             f"({len(dict_co2_by_country)})")

        list_country_by_co2 = sorted(dict_co2_by_country.items(), reverse=True,
                                     key=lambda tupl: tupl[1])
        x, y = list(map(list, zip(*list_country_by_co2)))
        if n < len(x):
            x, y = x[:n] + ['All other countries'], y[:n] + [sum(y[n:])]

        fig, ax = plt.subplots()
        colors = plt.get_cmap('tab20b')([0 + i/len(x) for i in range(len(x))])
        ax.bar(x, [ys/1000 for ys in y], color=colors)
        ax.set_title(f'Total emissions for each country (top {n})')
        ax.set_ylabel('Total emissions (tonnes CO2)')
        ax.tick_params(axis='x', labelrotation=70)

        if save:
            fig.savefig(f"./{host_city.name.lower().replace(' ','_')}.png")
        else:
            return fig
