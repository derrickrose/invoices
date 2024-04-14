import os
from datetime import datetime

INITIAL_DATE_FORMAT = "%d_%m_%Y"
INITIAL_DATE_REGEX = "\d{2}_\d{2}_\d{4}"
TARGET_DATE_FORMAT = '%Y-%m-%d'
INVOICES_DIRECTORY = '/home/frils/Documents/charges/2022/2022_ok/'

DATE_FORMAT_REGEX_MAPPING = {
    INITIAL_DATE_FORMAT: "\d{2}_\d{2}_\d{4}",
    TARGET_DATE_FORMAT: "\d{4}-\d{2}-\d{2}",
}


def convert_date(date: str, initial_format: str, target_format: str) -> str:
    return datetime.strptime(date, initial_format).strftime(target_format)


def build_new_name(file_name: str, initial_format, target_format) -> str:
    import re
    date_match = re.search(DATE_FORMAT_REGEX_MAPPING[initial_format], file_name)
    if date_match:
        date_raw = date_match.group()
        new_date_raw = convert_date(date_raw, initial_format, target_format)
        file_name = file_name.replace(date_raw, new_date_raw)
    return file_name


def iterate_and_update_files(path: str, initial_format, target_format):
    import glob
    for file in glob.glob(path, recursive=True):
        print(file)
        os.rename(file, build_new_name(file, initial_format, target_format))


if __name__ == "__main__":
    iterate_and_update_files(f"{INVOICES_DIRECTORY}*", INITIAL_DATE_FORMAT, TARGET_DATE_FORMAT)
