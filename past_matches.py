from os import listdir, path
from csv import DictReader

PAST_MATCHES_DIR_NAME = "previous_matches"

def create_past_matches_mapping():
    past_matches_map = {}
    # Iterate through the files of matching results from previous months to create mapping.
    for filename in listdir(PAST_MATCHES_DIR_NAME):
        with open(path.join(PAST_MATCHES_DIR_NAME, filename)) as f:
            _read_past_matches_file(DictReader(f), past_matches_map)
    return past_matches_map

def _read_past_matches_file(csv_reader, past_matches_map):
    """
    Mutates the `past_matches_map` with entries from the given CSV file.

    Parameters
    ----------
    csv_reader: csv.DictReader
        Reference to CSV file reader that iterates through the rows
    past_matches: Dict[str, List[str]]
        Result so far.
        Past matches dict of upper year names to list of lower year names.
    """
    # Create mapping of mentor to array of mentees for each row.
    for row in csv_reader:
        # Fetch previous values of mapping.
        mentor_name = row["Mentor name"]
        values = past_matches_map.get(mentor_name, list())

        # Append new values to existing keys instead of replacing.
        values.append(row["Mentee 1 name"])
        if row.get("Mentee 2 name"):
            values.append(row["Mentee 2 name"])
        
        past_matches_map[mentor_name] = values
