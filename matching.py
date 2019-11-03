import csv

from matcher import Matcher
from student import Student

lower_years = []
upper_years = []
ignored_words = ["I", "I'm", "and", "a", "to"]


def calculate_points(ranker, rankee):
    points = 0
    ranker_words = ranker.intro.split()
    rankee_words = rankee.intro.split()
    words_in_common = set(ranker_words).intersection(set(rankee_words))
    for word in ignored_words:
        words_in_common.discard(word)
    points += len(words_in_common)
    if ranker.should_match_with_same_gender:
        if ranker.gender == rankee.gender:
            points += 10
    return points


with open('signup_data/CS-Coffee-Chat_October-13-2019_10.10.csv', 'r') as f:
    reader = csv.reader(f)
    # Skip first 3 rows because they're all headers
    next(reader)
    next(reader)
    next(reader)
    for row in reader:
        year = 0
        if row[19] == "5+" or row[19] == "BCS":
            year = 5
        else:
            year = int(row[19])
        should_match_with_same_gender = False
        if row[22] == "Yes":
            should_match_with_same_gender = True
        student = Student(name=row[17], email=row[18], year=year, gender=row[20],
                          should_match_with_same_gender=should_match_with_same_gender, intro=row[23])
        if student.year < 3:
            lower_years.append(student)
        else:
            upper_years.append(student)

lower_year_rankings = {}
for lower_year in lower_years:
    current_rankings = {}
    for upperYear in upper_years:
        current_rankings[upperYear] = calculate_points(lower_year, upperYear)
    current_rankings = sorted(current_rankings.items(), key=lambda item: item[1], reverse=True)
    rankingsList = list(map(lambda key_value_pair: key_value_pair[0].name, current_rankings))
    lower_year_rankings[lower_year.name] = rankingsList

upper_year_rankings = {}
for upperYear in upper_years:
    current_rankings = {}
    for lower_year in lower_years:
        current_rankings[lower_year] = calculate_points(upperYear, lower_year)
    current_rankings = sorted(current_rankings.items(), key=lambda item: item[1], reverse=True)
    rankingsList = list(map(lambda key_value_pair: key_value_pair[0].name, current_rankings))
    upper_year_rankings[upperYear.name] = rankingsList

matcher = Matcher(upper_year_rankings, lower_year_rankings)
matches = matcher.match()
for index, match in enumerate(matches):
    print("{upperYear} with {lowerYear}".format(upperYear=upper_years[index].name, lowerYear=match))
