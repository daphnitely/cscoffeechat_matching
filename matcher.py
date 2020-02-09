from collections import defaultdict

class Matcher:
    """
    Logic derived from this gist: https://gist.github.com/joyrexus/9967709

    Attributes
    ----------
    upper_years: Dict[str, List[str]]
        Dict of upper year names to list of lower year names
    lower_years: Dict[str, List[str]]
        Dict of lower year names to list of upper year names
    urank: Dict[str, Dict[str, int]]
        Dict of upper year student name to (preferred student name, index) dict.
        `self.urank[student][other_student]` is student's ranking of other_student.
    lrank:
        Dict of lower year student name to (preferred student name, index) dict.
    """

    def __init__(self, upper_years, lower_years):
        """
        Constructs a Matcher instance.
        Takes a dict of upper_years's match preferences, `upper_years`,
        and a dict of lower_years's match preferences, `lower_years`.
        """
        self.U = upper_years
        self.L = lower_years

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
        lower_year: str
            Name of a lower year student
        u: str
            Name of a new upper year student
        h: str
            Name of an old upper year student

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
        str: Name of new lower year student
        """
        index = self.urank[upper_year][lower_year] + 1  # index of lower year following l in list of prefs
        return self.U[upper_year][index]

    def _match(self, past_matches, upper_years, next, matches):
        """
        Try to match all upper_years with their next preferred lower year student.

        Parameters
        ----------
        upper_years: List[str]
            List of upper year names.
        next: Dict[str, str]
            Dict of upper year students to their next preferred lower year student.
        matches: Dict[]
            Result so far

        Output
        ------
        Completed `matches` dictionary mapping lower year names to upper year names.
        """
        # if upper_years is empty, return matches found
        if not upper_years:
            return matches

        # get first and rest from upper_years list
        first_upper_year, rest = upper_years[0], upper_years[1:]
        u = first_upper_year

        # next lower year for first_upper_year to propose to
        next_lower_year = next[first_upper_year]  
        l = next_lower_year
        # set next to be lower year after next_lower_year in first_upper_year's list of prefs
        next[first_upper_year] = self.after(first_upper_year, next_lower_year)  

        if next_lower_year in matches:
            current_upper_match = matches[next_lower_year]  # current match
            if next_lower_year in past_matches.get(current_upper_match, list()):
                # if next_lower_year and current_upper_match had been matched in previous months
                rest.append(current_upper_match)  # match becomes available again
            if self.prefers(next_lower_year, first_upper_year, current_upper_match):
                rest.append(current_upper_match)  # match becomes available again
                # next_lower_year becomes match of first_upper_year
                matches[next_lower_year] = first_upper_year  
            else:
                rest.append(first_upper_year)  # first_upper_year remains unmatched
        else:
            # next_lower_year becomes match of first_upper_year
            matches[next_lower_year] = first_upper_year  
            
        return self._match(rest, next, matches)

    def match(self, past_matches):
        """
        Try to match all upper_years with their next preferred spouse.
        """
        # get the complete list of upper_years
        upper_years = list(self.U.keys())  
        # if not defined, map each upper year to their first preference
        next = {upper_year_student: ranks[0] for upper_year_student, ranks in self.U.items()}
        
        direct_matches = self._match(past_matches, upper_years, next, matches={})
        # get list of unmatched lower years
        unmatched = [lower_year for lower_year in self.L.keys() if lower_year not in direct_matches]
        return direct_matches

def _build_preferences(students):
    """
    Index matching preferences at initialization to avoid expensive lookups later.

    Parameters
    ----------
    students: Dict[str, List[str]]
        Either upper_years or lower_years
    """
    result = defaultdict(dict)
    for student_name, preferences in students.items():
        for index, preference_name in enumerate(preferences):
            result[student_name][preference_name] = index
    return result
