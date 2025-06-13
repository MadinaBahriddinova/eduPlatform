from __future__ import annotations
import datetime

class Grade:
    """
    Represents a specific grade given to a student for a subject.
    """
    _next_id = 1 # Class-level attribute to generate unique IDs for grades

    def __init__(self, student_id: int, subject: str, value: int, teacher_id: int, comment: str = None):
        """
        Initializes a Grade instance.
        Attributes:
        id: Unique grade ID (int)
        student_id: ID of the student who received the grade (int)
        subject: Subject the grade is for (str)
        value: Grade value (int, 1-5)
        date: Date the grade was given (str, ISO format)
        teacher_id: ID of the teacher who gave the grade (int)
        comment: Optional comment for the grade (str)
        """
        self._id = Grade._next_id
        Grade._next_id += 1
        self.student_id = student_id
        self.subject = subject
        self.value = value
        self.date = datetime.datetime.now().isoformat()
        self.teacher_id = teacher_id
        self.comment = comment

    @property
    def id(self) -> int:
        return self._id

    def update_grade(self, new_value: int, new_comment: str = None):
        """
        Updates the value and/or comment of the grade.
        """
        if not (1 <= new_value <= 5):
            print("Error: New grade value must be between 1 and 5.")
            return False
        self.value = new_value
        if new_comment is not None:
            self.comment = new_comment
        print(f"Grade {self.id} updated to {self.value} for student {self.student_id} in {self.subject}.")
        return True

    def get_grade_info(self) -> dict:
        """Returns a dictionary with grade details."""
        return {
            "id": self.id,
            "student_id": self.student_id,
            "subject": self.subject,
            "value": self.value,
            "date": self.date,
            "teacher_id": self.teacher_id,
            "comment": self.comment
        }