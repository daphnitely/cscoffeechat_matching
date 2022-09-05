def valid_filename(filename):
    """Check if filename is for a CSV file with no folder names."""
    return not "/" in filename and filename.endswith(".csv")

def duplicate_matches(past_matches, matches):
    matches_pairs = set(
        frozenset(s.email for s in students)
        for students in matches.items()
    )

    return not past_matches.isdisjoint(matches_pairs)

def unique_column_indexes(column_indexes):
    """
    Validates that all column indexes are unique.
    Repetition indicates an error with the input file or script.

    Parameters
    ----------
    column_indexes: Dict[str, list[int]]
    """
    items_list = list()
    for indexes in column_indexes.values():
        items_list.extend(indexes)

    return len(set(items_list)) == len(items_list)
