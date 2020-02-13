def valid_filename(filename):
    """Check if filename is for a CSV file with no folder names."""
    return not "/" in filename and filename.endswith(".csv")

def duplicate_matches(past_matches, matches):
    matches_pairs = set(
        frozenset(s.email for s in students)
        for students in matches.items()
    )
    
    return not past_matches.isdisjoint(matches_pairs)
