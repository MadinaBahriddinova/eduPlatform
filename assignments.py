from __future__ import annotations
import datetime
from enums import AssignmentDifficulty, AssignmentStatus
# Needed for type hinting in add_submission, etc.
# from users import User # Not strictly needed here, but might be useful for general user info


class Assignment:
    """
    Represents an assignment given to students.
    """
    _next_id = 1 # Class-level attribute to generate unique IDs for assignments

    def __init__(self, title: str, description: str, deadline: str, subject: str,
                 teacher_id: int, class_id: str, difficulty: AssignmentDifficulty):
        """
        Initializes an Assignment instance.
        Attributes:
        id: Unique assignment ID (int)
        title: Title of the assignment (str)
        description: Detailed description (str)
        deadline: Submission deadline (str, ISO format)
        subject: Subject the assignment belongs to (str)
        teacher_id: ID of the teacher who created it (int)
        class_id: Class/group the assignment is for (str)
        difficulty: Difficulty level (enum: AssignmentDifficulty)
        submissions: Dictionary of student submissions ({student_id: {'content': str, 'submitted_at': str, 'is_late': bool}})
        grades: Dictionary of grades for each student ({student_id: grade_value})
        """
        self._id = Assignment._next_id
        Assignment._next_id += 1
        self.title = title
        self.description = description
        self.deadline = deadline
        self.subject = subject
        self.teacher_id = teacher_id
        self.class_id = class_id
        self.difficulty = difficulty
        self.submissions = {} # {student_id: {'content': str, 'submitted_at': str, 'is_late': bool}}
        self.grades = {} # {student_id: grade_value}

    @property
    def id(self) -> int:
        return self._id

    def add_submission(self, student_id: int, content: str, is_late: bool = False):
        """
        Records a student's submission for this assignment.
        """
        self.submissions[student_id] = {
            'content': content,
            'submitted_at': datetime.datetime.now().isoformat(),
            'is_late': is_late
        }
        print(f"Submission for Assignment '{self.title}' by student {student_id} recorded.")


    def set_grade(self, student_id: int, grade_value: int):
        """
        Sets the grade for a student's submission.
        """
        if student_id not in self.submissions:
            print(f"Error: Student {student_id} has not submitted this assignment.")
            return

        if not (1 <= grade_value <= 5):
            print("Error: Grade value must be between 1 and 5.")
            return

        self.grades[student_id] = grade_value
        print(f"Grade {grade_value} set for student {student_id} on assignment '{self.title}'.")
        # In a more advanced system, this would trigger a notification to the student/parent

    def get_assignment_info(self) -> dict:
        """Returns a dictionary with assignment details."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline,
            "subject": self.subject,
            "teacher_id": self.teacher_id,
            "class_id": self.class_id,
            "difficulty": self.difficulty.value,
            "submissions_count": len(self.submissions),
            "grades_count": len(self.grades)
        }

    def get_submission_status(self, student_id: int) -> str:
        """
        Returns the submission status for a specific student.
        """
        if student_id not in self.submissions:
            return AssignmentStatus.PENDING.value
        
        if student_id in self.grades:
            return AssignmentStatus.GRADED.value
        
        if self.submissions[student_id].get('is_late', False):
            return AssignmentStatus.LATE_SUBMISSION.value
            
        return AssignmentStatus.SUBMITTED.value