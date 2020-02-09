from collections import defaultdict
from past_matches import past_matches_map 

# Logic derived from this gist: https://gist.github.com/joyrexus/9967709

class Matcher:
    def __init__(self, upper_years, lower_years):
        """
          Constructs a Matcher instance.
          Takes a dict of upper_years's match preferences, `upper_years`,
          and a dict of lower_years's match preferences, `lower_years`.
          """
        self.U = upper_years
        self.L = lower_years
        self.matches = {}
        self.pairs = []

        # we index matching preferences at initialization 
        # to avoid expensive lookups when matching
        self.urank = defaultdict(dict)  # `urank[u][l]` is u's ranking of l
        self.lrank = defaultdict(dict)  # `lrank[l][u]` is l's ranking of u

        for u, prefs in upper_years.items():
            for i, l in enumerate(prefs):
                self.urank[u][l] = i

        for l, prefs in lower_years.items():
            for i, u in enumerate(prefs):
                self.lrank[l][u] = i

    def __call__(self):
        return self.match()

    def prefers(self, l, u, h):
        """Test whether l prefers u over h."""
        return self.lrank[l][u] < self.lrank[l][h]

    def after(self, u, l):
        """Return the match favored by u after l."""
        i = self.urank[u][l] + 1  # index of lower year following l in list of prefs
        return self.U[u][i]

    def match(self, upper_years=None, next=None, matches=None):
        """
        Try to match all upper_years with their next preferred match.

        """
        if upper_years is None:
            upper_years = self.U.keys()  # get the complete list of upper_years
        if next is None:
            # if not defined, map each upper year to their first preference
            next = dict((u, rank[0]) for u, rank in self.U.items())
        if matches is None:
            matches = {}  # mapping from lowerYears to current match
        if not len(upper_years):
            self.pairs = [(curr, l) for l, curr in matches.items()]
            self.matches = matches
            return matches
        u, upper_years = list(upper_years)[0], list(upper_years)[1:]
        l = next[u]  # next lower year for u to match to
        next[u] = self.after(u, l)  # lower year after l in u's list of prefs
        if l in matches:
            curr = matches[l]  # current upper year match
            # If l and curr had been matched in previous months
            if curr in past_matches_map and l in past_matches_map[curr]:
                upper_years.append(curr)  # match becomes available again
            elif self.prefers(l, u, curr): 
                upper_years.append(curr)  # match becomes available again
                matches[l] = u  # l becomes match of u
            else:
                upper_years.append(u)  # u remains available
        else:
            matches[l] = u  # l becomes match of u
        return self.match(upper_years, next, matches)
