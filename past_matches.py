from os import listdir, path
from csv import DictReader
from itertools import combinations

PAST_MATCHES_DIR_NAME = "previous_matches"

def create_past_matches():
    """
    Returns a set of sets with students who have already met.

    The inner sets all contain exactly 2 items and are frozen.
    They act like unordered tuples.
    """

    past_matches_set = set()
    # Iterate through the files of matching results from previous months to create mapping.
    for filename in listdir(PAST_MATCHES_DIR_NAME):
        with open(path.join(PAST_MATCHES_DIR_NAME, filename)) as f:
            for pair in _read_past_matches_names(DictReader(f)):
                past_matches_set.add(pair)
    return past_matches_set

def _read_past_matches_names(csv_reader):
    """
    Yields pairs of student names who have already met.

    Parameters
    ----------
    csv_reader: csv.DictReader
        Reference to CSV file reader that iterates through the rows
    """
    # Create mapping of mentor to array of mentees for each row.
    for row in csv_reader:
        # Fetch previous values of mapping.
        mentor_name = row["Mentor name"]

        # Append new values to existing keys instead of replacing.
        yield frozenset([mentor_name, row["Mentee 1 name"]])
        if row.get("Mentee 2 name"):
            yield frozenset([mentor_name, row["Mentee 2 name"]])

def _read_past_matches_emails(csv_reader):
    """
    Yields pairs of student emails who have already met.

    Parameters
    ----------
    csv_reader: csv.DictReader
        Reference to CSV file reader that iterates through the rows.
    """
    # Create mapping of mentor to array of mentees for each row.
    for row in csv_reader:
        for combo in combinations(row["Emails"].split(", "), 2):
            yield frozenset(combo)          
