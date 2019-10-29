import os
import pickle
import csv
import pandas as pd
from student import Student

lower_years = []
upper_years = []

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
			lower_years.append(student)
		else:
			upper_years.append(student)

for student in lower_years:
	print(student.name)
	print(student.email)
	print(student.year)
	print(student.gender)
	print(student.shouldMatchWithSameGender)
	print(student.intro)
