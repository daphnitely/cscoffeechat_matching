from os import listdir, path
import csv
from datetime import datetime

from matcher import Matcher
from student import Student

SIGNUP_DATA_DIR_NAME = "signup_data"

NAME_COL = 17
EMAIL_COL = 18
YEAR_COL = 19
GENDER_COL = 20
SAME_GENDER_PREF_COL = 22
INTRO_COL = 23
STAY_ENROLLED_COL = 24

def _get_reader(file):
    """Get CSV reader and skip header rows."""
    reader = csv.reader(file)
    # Skip first 3 rows because they're all headers.
    for _ in range(3):
        next(reader)
    return reader

def _is_true(cell):
    return cell.strip() == "Yes"

def read_signup_data(current_month_file_name):
    """
    Read signup data from the CSV files in the signup_data folder.

    Parameters
    ----------
    current_month_file_name: string
        Name of the current month's CSV file.

    Output
    ------
    Set[Student], Set[Student] 
    Tuple of upper years and lower years.
    """

    # Build students lists and sets of student names
    lower_years = set()
    upper_years = set()

    def handle_student_row(row):
        student = student_from_row(row)
        target_set = lower_years if student.year < 3 else upper_years
        target_set.add(student)

    with open(path.join(SIGNUP_DATA_DIR_NAME, current_month_file_name), "r") as f:
        reader = _get_reader(f)
        for row in reader:
            handle_student_row(row)

    # Iterate through the files of signup data from previous months.
    for filename in listdir(SIGNUP_DATA_DIR_NAME):
        if filename != current_month_file_name and filename.endswith(".csv"):
            with open(path.join(SIGNUP_DATA_DIR_NAME, filename)) as f:
                reader = _get_reader(f)
                for row in reader:
                    # Add the students who want to stay enrolled in CS Coffee Chat.
                    if _is_true(row[STAY_ENROLLED_COL]):
                        handle_student_row(row)

    return (upper_years, lower_years)

def student_from_row(row):
    """Take in one row from the signup data and create a Student object from it."""
    year = 0
    # TODO: don't automatically put BCS into upper years.
    if row[YEAR_COL] == "5+" or row[YEAR_COL] == "BCS":
        year = 5
    else:
        year = int(row[YEAR_COL])

    return Student(
        name=row[NAME_COL], 
        email=row[EMAIL_COL], 
        year=year, 
        gender=row[GENDER_COL],
        should_match_with_same_gender=_is_true(row[SAME_GENDER_PREF_COL]), 
        intro=row[INTRO_COL]
    )
