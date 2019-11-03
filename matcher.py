from collections import defaultdict

'''
Logic derived from this gist: https://gist.github.com/joyrexus/9967709
'''
class Matcher:
  
    def __init__(self, upperYears, lowerYears):
        '''
        Constructs a Matcher instance.
        Takes a dict of upperYears's match preferences, `upperYears`,
        and a dict of lowerYears's match preferences, `lowerYears`.
        '''
        self.U = upperYears
        self.L = lowerYears
        self.matches = {}
        self.pairs = []

        # we index matching preferences at initialization 
        # to avoid expensive lookups when matching
        self.urank = defaultdict(dict)  # `urank[u][l]` is u's ranking of l
        self.lrank = defaultdict(dict)  # `lrank[l][u]` is l's ranking of u

        for u, prefs in upperYears.items():
            for i, l in enumerate(prefs):
                self.urank[u][l] = i

        for l, prefs in lowerYears.items():
            for i, u in enumerate(prefs):
                self.lrank[l][u] = i


    def __call__(self):
        return self.match()

    def prefers(self, l, u, h):
        '''Test whether l prefers u over h.'''
        return self.lrank[l][u] < self.lrank[l][h]

    def after(self, u, l):
        '''Return the match favored by u after l.'''
        i = self.urank[u][l] + 1    # index of lower year following l in list of prefs
        return self.U[u][i]

    def match(self, upperYears=None, next=None, matches=None):
        '''
        Try to match all upperYears with their next preferred spouse.
        
        '''
        if upperYears is None: 
            upperYears = self.U.keys()         # get the complete list of upperYears
        if next is None: 
            # if not defined, map each upper year to their first preference
            next = dict((u, rank[0]) for u, rank in self.U.items()) 
        if matches is None: 
            matches = {}                  # mapping from lowerYears to current match
        if not len(upperYears): 
            self.pairs = [(h, l) for l, h in matches.items()]
            self.matches = matches
            return matches
        u, upperYears = list(upperYears)[0], list(upperYears)[1:]
        l = next[u]                     # next lower year for u to propose to
        next[u] = self.after(u, l)      # lower year after l in u's list of prefs
        if l in matches:
            h = matches[l]                # current match
            if self.prefers(l, u, h):
                upperYears.append(h)           # match becomes available again
                matches[l] = u            # l becomes match of u
            else:
                upperYears.append(u)           # u remains unmarried
        else:
            matches[l] = u                # l becomes match of u
        return self.match(upperYears, next, matches)

    # def is_stable(self, matches=None, verbose=False):
    #     if matches is None:
    #         matches = self.matches
    #     for l, u in matches.items():
    #         i = self.U[u].index(l)
    #         preferred = self.U[u][:i]
    #         for p in preferred:
    #             h = matches[p]
    #             if self.L[p].index(u) < self.L[p].index(h):  
    #                 msg = "{}'s marriage to {} is unstable: " + \
    #                       "{} prefers {} over {} and {} prefers " + \
    #                       "{} over her current husband {}"
    #                 if verbose:
    #                     print msg.format(u, l, u, p, l, p, u, h) 
    #                 return False
    #     return True