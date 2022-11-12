# pylint: disable = C0114, C0116
from typing import List, Tuple
from pathlib import Path
import csv
from cities import City, CityCollection


def read_attendees_file(filepath: Path) -> CityCollection:
    if not isinstance(filepath, Path) and not isinstance(filepath, str):
        raise TypeError("File path should be given as a pathlib.Path object "
                        "or a string")

    with open(filepath, 'r', encoding="utf-8") as attendees_file:
        csv_reader = csv.reader(attendees_file)
        attendees_raw_data = [record for record in csv_reader]

    # Checking the order in which the columns are arranged in the attendees
    # raw data
    ordered_fieldnames = [('city', str), ('country', str), ('N', int),
                          ('lat', float), ('lon', float)]
    ordered_col_indexes = [attendees_raw_data[0].index(fieldname)
                           for required_fieldname, _ in ordered_fieldnames
                           for fieldname in attendees_raw_data[0]
                           if fieldname == required_fieldname]

    # Rearranging the columns in the attendees raw data so they match the order
    # expected in the City object's input
    cities_ordered_data = [tuple([row[i] for i in ordered_col_indexes])
                           for row in attendees_raw_data[1:]]

    # Changing columns to appropriate data types for the City object's input
    # and carrying out some additional type tests on the instances
    cits, countrs, ns, lats, longs = list(map(list, zip(*cities_ordered_data)))
    cits, countrs, ns, lats, longs = assign_cities_data_types(cits, countrs,
                                                              ns, lats, longs)
    city_assigned_type_data = list(zip(cits, countrs, ns, lats, longs))

    city_objects_list = [City(*city_data)
                         for city_data in city_assigned_type_data]

    return CityCollection(city_objects_list)


def assign_cities_data_types(cits: List[str], countrs: List[str],
                             ns: List[str], lats: List[str], longs: List[str]
                             ) -> Tuple[List[str], List[str], List[int],
                                        List[float], List[float]]:
    numbers = [str(num) for num in range(10)]

    for i, _ in enumerate(cits):
        try:
            if (any([num in cits[i] for num in numbers])
                and cits[i] != ('Skrzatow '
                                '1')):
                raise TypeError('String contains numbers')
        except Exception as err:
            raise TypeError(f"City '{cits[i]}' in row {i + 2} should be "
                            "written as a string") from err
        try:
            if any([num in countrs[i] for num in numbers]):
                raise TypeError('String contains numbers')
        except Exception as err:
            raise TypeError(f"Country '{countrs[i]}' in row {i + 2} should be "
                            "written as a string") from err
        try:
            if '.' in ns[i]:
                raise TypeError('Integer contains decimal point')
            if not all([any([num in letter for num in numbers])
                        for letter in ns[i]]):
                raise TypeError('Integer contains character')
            ns[i] = int(ns[i])  # type: ignore
        except Exception as err:
            raise TypeError(f"Number of attendees '{ns[i]}' in row {i + 2} "
                            "should be written as an integer") from err
        try:
            if '.' not in lats[i]:
                raise TypeError('Floating point number is missing a '
                                'decimal point')
            if not all([any([num in letter for num in (numbers + ['.', '-'])])
                        for letter in lats[i]]):
                raise TypeError('Floating point number contains character')
            lats[i] = float(lats[i])  # type: ignore
        except Exception as err:
            raise TypeError(f"Latitude '{lats[i]}' in row {i + 2} should be "
                            "written as a floating point number") from err
        try:
            if '.' not in longs[i]:
                raise TypeError('Floating point number is missing a '
                                'decimal point')
            if not all([any([num in letter for num in (numbers + ['.', '-'])])
                        for letter in longs[i]]):
                raise TypeError('Floating point number contains character')
            longs[i] = float(longs[i])  # type: ignore
        except Exception as err:
            raise TypeError(f"Longitude '{longs[i]}' in row {i + 2} should be "
                            "written as a floating point number") from err

    return cits, countrs, ns, lats, longs  # type: ignore
