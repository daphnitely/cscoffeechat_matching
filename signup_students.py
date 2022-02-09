from os import listdir, path
import csv
from datetime import datetime

from matcher import Matcher
from student import Student
from validate import unique_items

SIGNUP_DATA_DIR_NAME = "signup_data"

# Map of column names in the CSV files.
# Names just need to partially match
# (i.e. "your gender" in "What's your gender?")
column_names = {
    'name': "What's your full name",
    'email': "What's your email address",
    'year': "What year are you in",
    'gender': "What is your gender",
    'same_gender_pref': "Would you prefer to be matched with someone of the same gender",
    'intro': "Introduce yourself",
    'stay_enrolled': "Would you like to stay enrolled for "
}

def _format_year(raw_year):
    year = 0
    # Chop off the "Year" prefix
    if raw_year.lower().startswith("year "):
        raw_year = raw_year[len("year "):]

    # TODO: don't automatically put BCS into upper years.
    if raw_year == "5+" or raw_year == "BCS":
        year = 5
    else:
        year = int(raw_year)
    return year

def _read_csv(file, header_index=0, skip_until_index=1):
    """
    Yield CSV rows as students, while skipping header rows

    Parameters
    ----------
    file: file object
        CSV file to read
    header_index: int
        Row index of the header in the CSV file.
    skip_until_index: int
        Row index where data starts in the CSV file.
        Useful if there are unneeded rows in the CSV you want to ignore.
    """

    reader = csv.reader(file)
    # Default column values
    column_indexes = {}

    def get_csv_value(row, column_name, optional=False):
        column_index = column_indexes.get(column_name)
        if column_index is None:
            if optional:
                return None
            else:
                raise RuntimeError(f"Could not find {column_name} column in {file.name}")
        return row[column_index]

    for i, row in enumerate(reader):
        if i == header_index:
            # Store headers
            headers = row
            # Find column numbers
            for column_name, known_header in column_names.items():
                for column_index, header_value in enumerate(headers):
                    if known_header in header_value:
                        column_indexes[column_name] = column_index
                        break
            print(column_indexes)
            # Make sure we don't reuse column indexes
            if not unique_items(column_indexes.values()):
                raise RuntimeError(f"Could not automatically figure out column indexes in {file.name}")
        elif i >= skip_until_index:
            # Process data row
            yield Student(
                name=get_csv_value(row, 'name'), 
                email=get_csv_value(row, 'email'), 
                year=_format_year(get_csv_value(row, 'year')), 
                gender=get_csv_value(row, 'gender'),
                should_match_with_same_gender=_is_true(get_csv_value(row, 'same_gender_pref')), 
                intro=get_csv_value(row, 'intro', optional=True) or "",
                stay_enrolled=get_csv_value(row, 'stay_enrolled', optional=True) or False
            )

def _is_true(cell):
    return cell.strip().lower() == "yes"

def read_signup_data(current_month_file_name):
    """
    Read signup data from the CSV files in the signup_data folder.

    Parameters
    ----------
    current_month_file_name: string
        Name of the current month's CSV file.
        File must be inside "signup_data" folder.

    Output
    ------
    Set[Student], Set[Student] 
    Tuple of upper years and lower years.

    Raises
    ------
    FileNotFoundError: If input file does not exist
    """

    # Build students lists and sets of student names
    lower_years = set()
    upper_years = set()

    def handle_student_row(student):
        target_set = lower_years if student.year < 3 else upper_years
        target_set.add(student)

    with open(path.join(SIGNUP_DATA_DIR_NAME, current_month_file_name), "r") as f:
        for student in _read_csv(f):
            handle_student_row(student)

    # Iterate through the files of signup data from previous months.
    for filename in listdir(SIGNUP_DATA_DIR_NAME):
        if filename != current_month_file_name and filename.endswith(".csv"):
            with open(path.join(SIGNUP_DATA_DIR_NAME, filename)) as f:
                for student in _read_csv(f):
                    # Add the students who want to stay enrolled in CS Coffee Chat.
                    if student.stay_enrolled:
                        handle_student_row(student)

    return (upper_years, lower_years)
