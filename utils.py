# pylint: disable = C0114, C0116
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

    raise NotImplementedError
