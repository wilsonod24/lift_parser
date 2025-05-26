from dataclasses import dataclass
import datetime

@dataclass
class WorkoutSet:
    date: datetime.date
    exercise: str
    set_number: int
    reps: float
    weight_lbs: float
    notes: str = ''

    def __str__(self):
        return (
            f"Date: {self.date}\n\t"
            f"Exercise: {self.exercise}\n\t"
            f"Set Number: {self.set_number}\n\t"
            f"Reps: {self.reps}\n\t"
            f"Weight in Lbs: {self.weight_lbs}\n\t"
            f"Notes: {self.notes}"
        )
    