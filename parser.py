import re
import models
from datetime import date, datetime

def parse_exercise(line: str, date: date = date.today()) -> list[models.WorkoutSet]:

    # Split the line into DB Bench w 70s and 8/6/5
    parts = re.split(r'\s*(\-|:)\s*', line)

    # Split the sets into a list of individual reps per set
    set_reps = parts[-1].split('/')
    # Convert the list of strings (Reps) into integers
    int_list = []
    for s in set_reps:
        match = re.search(r'\d+\.?\d*', s)
        if match:
            int_list.append(int(match.group()))
    set_reps = int_list

    # Find the location where the weight starts
    match = re.search(r'(?=\d)', parts[0])
    
    if match:
        index = match.start()
        exercise = parts[0][:index].strip().lower()
        weight = parts[0][index:].strip().lower()
    else:
        exercise = parts[0].strip().lower()
        weight = ''

    # Remove with, w, w/, and @ from the exercise name
    exercise = re.split(r'\s+(w/|with|w|@|bw|at|\(|\+)\s*', exercise)[0].title()

    # remove any parenthesis and other things not needed
    weight = re.sub(r'\s*(\+|\()\s*','', weight)
    if weight.endswith('lbs'):
        match = re.search(r'\d+\.?\d*', weight)
        if match:
            weight_lbs = float(match.group())       
        else: 
            weight_lbs = 0

    elif weight.endswith('s'):
        match = re.search(r'\d+\.?\d*', weight)
        if match:
            weight_lbs = float(match.group()) * 2
        else: 
            weight_lbs = 0
    else:
        match = re.search(r'\d+\.?\d*', weight)
        if match:
            weight_lbs = float(match.group())
        else: 
            weight_lbs = 0

    # Create a list of sets
    sets = []
    set_number = 1
    # Add each set to the new list of sets
    for reps in set_reps:
        sets.append(
            models.WorkoutSet(
                date=date, exercise=exercise, 
                set_number = set_number, reps=reps, 
                weight_lbs=weight_lbs))
        set_number += 1

    return sets

def is_date(line: str):
    """Returns whether the string passed in is a date"""
    formats = [r"%m/%d/%Y", r"%m/%d/%y", r"%-m/%-d/%Y", r"%-m/%-d/%y"] # For handling many formats

    for fmt in formats:
        try:
            return datetime.strptime(line.strip(), fmt).date()
        except Exception as e:
            continue



def is_exercise_line(line):
    """check if the line has at least two rep numbers and has text"""
    return re.search(r'.*[A-Za-z\(\)@\-]+.*\d+(\.\d+)?(?:/\d+(\.\d+)?)+', line) is not None
