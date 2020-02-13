from collections import defaultdict

class Matcher:
    """
    Logic derived from this gist: https://gist.github.com/joyrexus/9967709

    Attributes
    ----------
    U: Dict[Student, List[Student]]
        Dict of upper years to list of lower years
    L: Dict[Student, List[Student]]
        Dict of lower years to list of upper years
    past_matches: Set[Set[string]]
        Set of student name pairs reprenting students matched in the past.
    urank: Dict[Student, Dict[Student, int]]
        Dict of upper year students to (preferred student, index) dict.
        `self.urank[student][other_student]` is student's ranking of other_student.
    lrank: Dict[Student, Dict[Student, int]]
        Dict of lower year students to (preferred student, index) dict.
    """

    def __init__(self, upper_years, lower_years, past_matches):
        """
        Constructs a Matcher instance.
        Takes a dict of upper_years's match preferences, `upper_years`,
        a dict of lower_years's match preferences, `lower_years`,
        and a dict of past upper_years to lower_years matchings.
        """
        self.U = upper_years
        self.L = lower_years
        self.past_matches = past_matches

        # we index matching preferences at initialization
        # to avoid expensive lookups when matching
        self.urank = _build_preferences(upper_years)
        self.lrank = _build_preferences(lower_years)

    def __call__(self):
        return self.match()

    def prefers(self, lower_year, u, h):
        """
        Test whether lower_year prefers u over h.

        Parameters
        ----------
        lower_year: Student
            A lower year student
        u: Student
            A new upper year student
        h: Student
            An old upper year student

        Output
        ------
        bool
        """
        return self.lrank[lower_year][u] < self.lrank[lower_year][h]

    def after(self, upper_year, lower_year):
        """
        Return the match favored by upper_year after lower_year.

        Output
        ------
        Student: New lower year student
        """
        index = self.urank[upper_year][lower_year] + 1  # index of lower year following l in list of prefs
        try:
            return self.U[upper_year][index]
        except IndexError:
            return None

    def previously_matched(self, upper, lower):
        return frozenset([upper.email, lower.email]) in self.past_matches

    def _match(self, upper_years, next, matches):
        """
        Try to match all upper_years with their next preferred lower year student.

        Parameters
        ----------
        upper_years: List[Student]
            List of upper year names.
        next: Dict[Student, Student]
            Dict of upper year students to their next preferred lower year student.
        matches: Dict[Student, Student]
            Result so far

        Output
        ------
        Completed `matches` dictionary mapping lower years to upper years.
        """
        # if upper_years is empty, return matches found
        if not upper_years:
            return matches

        # get first and rest from upper_years list
        first_upper_year, rest = upper_years[0], upper_years[1:]

        # next lower year for first_upper_year to propose to
        next_lower_year = next[first_upper_year]  
        # set next to be lower year after next_lower_year in first_upper_year's list of prefs
        if next_lower_year is not None:
            next[first_upper_year] = self.after(first_upper_year, next_lower_year)  

        if next_lower_year in matches:
            current_upper_match = matches[next_lower_year]  # current match
            if self.previously_matched(current_upper_match, next_lower_year):
                # if next_lower_year and current_upper_match had been matched in previous months
                rest.append(current_upper_match)  # match becomes available again
                matches[next_lower_year] = first_upper_year
            elif self.prefers(next_lower_year, first_upper_year, current_upper_match):
                rest.append(current_upper_match)  # match becomes available again
                # next_lower_year becomes match of first_upper_year
                matches[next_lower_year] = first_upper_year
            else:
                rest.append(first_upper_year)  # first_upper_year remains unmatched
        elif next_lower_year is not None:
            # next_lower_year becomes match of first_upper_year
            matches[next_lower_year] = first_upper_year  
            
        return self._match(rest, next, matches)

    def match(self):
        """
        Try to match all upper_years with their next preferred spouse.

        Output
        ------
        Dict[Student, Student]
        Completed `matches` dictionary mapping lower years to upper years.
        """
        # get the complete list of upper_years
        upper_years = list(self.U.keys())
        # if not defined, map each upper year to their first preference
        next = {upper_year_student: ranks[0] for upper_year_student, ranks in self.U.items()}

        direct_matches = self._match(upper_years, next, matches={})
        # get list of unmatched lower years
        unmatched_lower = [lower_year.name for lower_year in self.L.keys() if lower_year not in direct_matches]
        unmatched_upper = [upper_year.name for upper_year in self.U.keys() if upper_year not in direct_matches.values()]
        print('Unmatched lower years', unmatched_lower)
        print('Unmatched upper years', unmatched_upper)
        return direct_matches

def _build_preferences(students):
    """
    Index matching preferences at initialization to avoid expensive lookups later.

    Parameters
    ----------
    students: Dict[Student, List[Student]]
        Either upper_years or lower_years

    Output
    ------
    Dict[Student, Dict[Student, int]]
    """
    result = defaultdict(dict)
    for student, preferences in students.items():
        for index, preference in enumerate(preferences):
            result[student][preference] = index
    return result
