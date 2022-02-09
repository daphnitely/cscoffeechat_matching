from dataclasses import dataclass

# These are words that will appear in most intros, and should be ignored when calculating
# the similarity score.
# TODO: improve the set of words that we should ignore.
IGNORED_WORDS = set(["I", "I'm", "and", "a", "to"])

@dataclass
class Student:
    name: str = ""
    email: str = ""
    year: int = 1
    gender: str = "Female"
    should_match_with_same_gender: bool = False
    intro: str = ""
    stay_enrolled: bool = False

    def __eq__(self, other):
        return self.email == other.email

    def __hash__(self):
        return hash(self.email)

def build_rankings(from_students, to_students):
    """
    Build dictionary of students to list of their preferred students, in order.

    Parameters
    ----------
    from_students: Iterable[Student]
        These students are the rankers, used as dict keys
    to_students: Iterable[Student]
        These students are the rankees, used as dict values

    Output
    ------
    Dict[Student, List[Student]]
    """

    def getvalue(pair):
        return pair[1]

    rankings = {}
    for student in from_students:
        student_rankings = {}
        for other_student in to_students:
            student_rankings[other_student] = _calculate_points(student, other_student)
        student_rankings_pairs = sorted(student_rankings.items(), key=getvalue, reverse=True)
        student_rankings_list = [other for other, _ in student_rankings_pairs]
        rankings[student] = student_rankings_list
    return rankings

def _calculate_points(ranker, rankee):
    """
    Quantify how much the ranker might prefer to be matched with the rankee based on
    whether or not the ranker has a gender preference, and how similar their intros are.
    """
    # Add points based on words shared in intros
    points = 0
    ranker_words = set(ranker.intro.split())
    rankee_words = set(rankee.intro.split())
    words_in_common = ranker_words.intersection(rankee_words).difference(IGNORED_WORDS)
    points += len(words_in_common)

    # Add points if gender preferences match
    if ranker.should_match_with_same_gender and ranker.gender == rankee.gender:
        points += 10

    return points
