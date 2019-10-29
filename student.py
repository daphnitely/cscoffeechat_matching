from enum import Enum
class Student:
    name = ""
    email = ""
    year = 1
    gender = "Female"
    shouldMatchWithSameGender = False
    intro = ""


    def __init__(self, name, email, year, gender, shouldMatchWithSameGender, intro):
        self.name = name
        self.email = email
        self.year = year
        self.gender = gender
        self.shouldMatchWithSameGender = shouldMatchWithSameGender
        self.intro = intro