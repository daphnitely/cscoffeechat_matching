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
	lowerYearRankings[lowerYear] = sorted(currentRankings.items(), key=lambda item: item[1], reverse=True)

upperYearRankings = {}
for upperYear in upperYears:
	currentRankings = {}
	for lowerYear in lowerYears:
		currentRankings[lowerYear] = calculatePoints(upperYear, lowerYear)
	upperYearRankings[upperYear] = sorted(currentRankings.items(), key=lambda item: item[1], reverse=True)

for x in upperYearRankings:
	print(x)
	for y in upperYearRankings[x]:
  		print(y)
	
