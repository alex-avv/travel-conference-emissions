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

    raise NotImplementedError
