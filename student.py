from enum import Enum


class Student:
    name = ""
    email = ""
    year = 1
    gender = "Female"
    should_match_with_same_gender = False
    intro = ""

    def __init__(self, name, email, year, gender, should_match_with_same_gender, intro):
        self.name = name
        self.email = email
        self.year = year
        self.gender = gender
        self.should_match_with_same_gender = should_match_with_same_gender
        self.intro = intro
