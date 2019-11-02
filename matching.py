import os
import pickle
import csv
import pandas as pd
from student import Student

lowerYears = []
upperYears = []

def calculatePoints(ranker, rankee):
	points = 0
	rankerWords = ranker.intro.split()
	rankeeWords = rankee.intro.split()
	common = set(rankerWords).intersection(set(rankeeWords))
	common.discard("I")
	common.discard("I'm")
	common.discard("and")
	common.discard("a")
	common.discard("to")
	points += len(common)
	if ranker.shouldMatchWithSameGender:
  		if ranker.gender == rankee.gender:
  				points += 10
	return points

def prefers(lrank, lowerYear, upperYear1, upperYear2):
  '''Test whether lowerYear prefers upperYear1 over upperYear2.'''
  return lrank[lowerYear][upperYear1] < lrank[lowerYear][upperYear2]

def after(urank, upperYear, lowerYear):
  '''Return the woman favored by m after w.'''
  i = urank[upperYear][lowerYear] + 1    # index of woman following w in list of prefs
  return upperYearRankings[upperYear][i]

# def match(upperYears=None, next=None, lowerYear=None):
#   '''
#   Try to match all men with their next preferred spouse.  
#   '''
#   if upperYears is None: 
#       upperYears = self.M.keys()         # get the complete list of men
#         if next is None: 
#             # if not defined, map each man to their first preference
#             next = dict((m, rank[0]) for m, rank in self.M.items()) 
#         if wives is None: 
#             wives = {}                  # mapping from women to current spouse
#         if not len(men): 
#             self.pairs = [(h, w) for w, h in wives.items()]
#             self.wives = wives
#             return wives
#         m, men = men[0], men[1:]
#         w = next[m]                     # next woman for m to propose to
#         next[m] = self.after(m, w)      # woman after w in m's list of prefs
#         if w in wives:
#             h = wives[w]                # current husband
#             if self.prefers(w, m, h):
#                 men.append(h)           # husband becomes available again
#                 wives[w] = m            # w becomes wife of m
#             else:
#                 men.append(m)           # m remains unmarried
#         else:
#             wives[w] = m                # w becomes wife of m
#         return self.match(men, next, wives)

with open('signup_data/CS-Coffee-Chat_October-13-2019_10.10.csv', 'r') as f:
	reader = csv.reader(f)
    # Skip first 3 rows because they're all headers
	next(reader)
	next(reader)
	next(reader)
	for row in reader:
		year = 0
		if (row[19] == "5+" or row[19] == "BCS"):
			year = 5
		else:
			year = int(row[19])
		shouldMatchWithSameGender = False
		if (row[22] == "Yes"):
			shouldMatchWithSameGender = True
		student = Student(name=row[17], email=row[18], year=year, gender=row[20], shouldMatchWithSameGender=shouldMatchWithSameGender, intro=row[23])
		if student.year < 3:
			lowerYears.append(student)
		else:
			upperYears.append(student)

lowerYearRankings = {}
for lowerYear in lowerYears:
	currentRankings = {}
	for upperYear in upperYears:
		currentRankings[upperYear] = calculatePoints(lowerYear, upperYear)
	currentRankings = sorted(currentRankings.items(), key=lambda item: item[1], reverse=True)
	rankingsList = map(lambda keyValuePair: keyValuePair[0], currentRankings)
	lowerYearRankings[lowerYear] = rankingsList

upperYearRankings = {}
for upperYear in upperYears:
	currentRankings = {}
	for lowerYear in lowerYears:
		currentRankings[lowerYear] = calculatePoints(upperYear, lowerYear)
	currentRankings = sorted(currentRankings.items(), key=lambda item: item[1], reverse=True)
	rankingsList = map(lambda keyValuePair: keyValuePair[0], currentRankings)
	upperYearRankings[upperYear] = rankingsList

for x in upperYearRankings:
	print(x)
	for y in upperYearRankings[x]:
  		print(y)

# urank = {}
# lrank = {}

# for upperYear, prefs in upperYearRankings.items():
# 	for i, lowerYear in enumerate(prefs):
# 		urank[upperYear][lowerYear] = i

# for lowerYear, prefs in lowerYearRankings.items():
# 	for i, upperYear in enumerate(prefs):
# 		lrank[lowerYear][upperYear] = i
	
