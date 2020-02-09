MENTOR_NAME = "Mentor name"
MENTEE_1_NAME = "Mentee 1 name"
MENTEE_2_NAME = "Mentee 2 name"

def create_past_matches_mapping(reader, past_matches_map): 
    # Find the columns for mentor and mentees names.
    # Skip the first row because it is header.
    header = next(reader)
    for num, name in enumerate(header):
        if name == MENTOR_NAME:
            MENTOR_NAME_COL = num
        elif name == MENTEE_1_NAME:
            MENTEE_1_NAME_COL = num
        else: 
            MENTEE_2_NAME_COL = num
    # Create mapping of mentor to array of mentees for each row.
    for row in reader:
        # Fetch previous values of mapping.
        if row[MENTOR_NAME_COL] in past_matches_map.keys():
            values = past_matches_map[row[MENTOR_NAME_COL]]
        else: 
            values = []

        # Append new values to existing keys instead of replacing.
        values.append(row[MENTEE_1_NAME_COL])
        if row[MENTEE_2_NAME_COL] != '':
            values.append(row[MENTEE_2_NAME_COL])
        past_matches_map[row[MENTOR_NAME_COL]] = values