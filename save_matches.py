from os.path import join
from csv import DictWriter
from datetime import datetime

MATCHING_DATA_DIR_NAME = "matching_data"

fields = ["Emails", "Mentor name", "Mentee 1 name"]

def default_output_name(time=datetime.now()):
    current_month = time.strftime("%B")
    current_year = time.strftime("%Y")
    return f"{current_month}_{current_year}_matching.csv"

def save_matching_data(matches, output_file_name):
    """
    Saves the given `matches` to a new CSV file in matching_data.

    Parameters
    ----------
    matches: Dict[Student, Student]
        Dict mapping lower years to upper years.
    output_file_name: str
        File name to save data to.
    """
    with open(join(MATCHING_DATA_DIR_NAME, output_file_name), "w+", newline='') as f:
        writer = DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for lower_year, upper_year in matches.items():
            # print(f"{upper_year.name} with {lower_year.name}")
            writer.writerow({
                "Emails": ", ".join([upper_year.email, lower_year.email]), 
                "Mentor name": upper_year.name, 
                "Mentee 1 name": lower_year.name
            })
    f.close()
