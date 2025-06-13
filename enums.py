from enum import Enum

class UserRole(Enum):
    """Defines the different roles for users in the EduPlatform."""
    ADMIN = "Admin"
    TEACHER = "Teacher"
    STUDENT = "Student"
    PARENT = "Parent"

class AssignmentDifficulty(Enum):
    """Defines the difficulty levels for assignments."""
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"

class AssignmentStatus(Enum):
    """Defines the possible statuses of an assignment."""
    PENDING = "Pending"
    SUBMITTED = "Submitted"
    GRADED = "Graded"
    LATE_SUBMISSION = "Late Submission" # Added for late submissions