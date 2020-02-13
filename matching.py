from argparse import ArgumentParser

from matcher import Matcher
from student import Student, build_rankings
from past_matches import create_past_matches_mapping
from signup_students import read_signup_data
from save_matches import save_matching_data, default_output_name
from validate import valid_filename

def main(input="coffee-2020-02.csv", output=default_output_name()):
    if not valid_filename(input) or not valid_filename(output):
        raise ValueError("Invalid input or output name")

    past_matches_map = create_past_matches_mapping()
    upper_years, lower_years = read_signup_data(input)

    lower_year_rankings = build_rankings(lower_years, upper_years)
    upper_year_rankings = build_rankings(upper_years, lower_years)

    # matches is a list of lower year students, ordered based on which upper year student
    # they are matched with.
    matcher = Matcher(upper_year_rankings, lower_year_rankings, past_matches_map)
    matches = matcher.match()

    save_matching_data(matches, output)

if __name__ == "__main__":
    parser = ArgumentParser(description="Run coffee chat matching.")
    parser.add_argument("-i", "--input", help="Name of the current month's signup data file.")
    parser.add_argument("-o", "--output", help="Name of the current month's matching data file.")
    args = parser.parse_args()

    main(args.input, args.output)
