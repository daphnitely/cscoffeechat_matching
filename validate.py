def valid_filename(filename):
    """Check if filename is for a CSV file with no folder names."""
    return not "/" in filename and filename.endswith(".csv")