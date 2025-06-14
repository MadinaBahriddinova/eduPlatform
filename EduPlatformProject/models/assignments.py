# models/assignments.py
import json
import datetime
from core.enums import AssignmentDifficulty, AssignmentStatus # Assuming these are defined here

class Assignment:
    _next_id = 1

    def __init__(self, teacher_id: int, title: str, description: str, deadline: str, # deadline received as string
                 subject: str, class_id: str, difficulty: AssignmentDifficulty):
        self._id = Assignment._next_id
        Assignment._next_id += 1
        self._teacher_id = teacher_id
        self._title = title
        self._description = description
        
        # --- CRITICAL FIX: ROBUST DEADLINE PARSING ---
        # Attempt to parse as date first (YYYY-MM-DD)
        try:
            self._deadline = datetime.datetime.strptime(deadline, "%Y-%m-%d").date()
        except ValueError:
            # If that fails, try to parse as a full ISO datetime string (YYYY-MM-DDTHH:MM:SS.ffffff)
            # and then extract just the date part. This handles what datetime.datetime.now().isoformat() produces.
            try:
                self._deadline = datetime.datetime.fromisoformat(deadline).date()
                # Optionally, add a less severe warning here if you want to know it had a time component
                # print(f"Note: Deadline '{deadline}' had time component, but was successfully converted to date.")
            except ValueError:
                # If both parsing attempts fail, store it as a string and print an error.
                # This should ideally not happen if you pass valid date/datetime strings.
                self._deadline = deadline # Fallback to string, but this is problematic for comparisons
                print(f"ERROR: Invalid deadline format '{deadline}'. Storing as string, which may cause errors later.")
        
        self._subject = subject
        self._class_id = class_id
        self._difficulty = difficulty
        self._submissions = {} # {student_id: {"content": str, "timestamp": str, "is_late": bool}}
        self._grades = {}      # {student_id: int}
        self._status = AssignmentStatus.PENDING # Initial status

    # --- Properties and Methods (rest of your Assignment class) ---

    @property
    def id(self) -> int:
        return self._id

    @property
    def teacher_id(self) -> int:
        return self._teacher_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def deadline(self) -> datetime.date: # <--- THIS MUST RETURN A datetime.date OBJECT
        """Returns the deadline as a datetime.date object."""
        # Ensure it's a date object if for some reason it's still a string (due to prior error)
        if isinstance(self._deadline, str):
            # This block should ideally not be hit if the __init__ parsing is robust.
            # But as a fallback, try to convert it here too.
            try:
                return datetime.datetime.fromisoformat(self._deadline).date()
            except ValueError:
                # If even this fails, raise an error or return a default/None
                print(f"Critical Error: Assignment {self.id} deadline '{self._deadline}' could not be parsed as date.")
                # Decide how to handle: raise, return None, or a default date
                return datetime.date.min # Or raise ValueError("Invalid deadline format")
        return self._deadline

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def class_id(self) -> str:
        return self._class_id

    @property
    def difficulty(self) -> AssignmentDifficulty:
        return self._difficulty

    @property
    def status(self) -> AssignmentStatus:
        return self._status

    @property
    def submissions(self) -> dict:
        return self._submissions

    @property
    def grades(self) -> dict:
        return self._grades

    def add_submission(self, student_id: int, content: str, is_late: bool = False):
        timestamp = datetime.datetime.now().isoformat()
        self._submissions[student_id] = {
            "content": content,
            "timestamp": timestamp,
            "is_late": is_late
        }
        if is_late:
            self._status = AssignmentStatus.LATE_SUBMISSION
        else:
            self._status = AssignmentStatus.SUBMITTED # Status for the assignment as a whole

    def set_grade(self, student_id: int, grade_value: int):
        if student_id in self._submissions:
            self._grades[student_id] = grade_value
            self._status = AssignmentStatus.GRADED # Update assignment status
            print(f"Grade {grade_value} set for student {student_id} on assignment {self.id}.")
        else:
            print(f"Error: Student {student_id} has no submission for assignment {self.id}.")

    def get_assignment_info(self) -> dict:
        """Returns a dictionary with assignment details for export."""
        # Ensure deadline is formatted as a string for export if it's a date object
        deadline_str = self.deadline.isoformat() if isinstance(self.deadline, datetime.date) else str(self.deadline)

        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": deadline_str, # Use the string representation for export
            "subject": self.subject,
            "teacher_id": self.teacher_id,
            "class_id": self.class_id,
            "difficulty": self.difficulty.value,
            "status": self.status.value,
            "submissions": json.dumps(self.submissions), # Serialize complex types for export
            "grades": json.dumps(self.grades)            # Serialize complex types for export
        }