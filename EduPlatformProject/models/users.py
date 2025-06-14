from __future__ import annotations

import hashlib
import datetime
import json  # <--- ADDED: Import for JSON serialization
from abc import ABC, abstractmethod
from core.enums import UserRole, AssignmentDifficulty, AssignmentStatus
from core.notifications import Notification
from models.assignments import Assignment  # Corrected import for Assignment model
from models.grades import Grade            # Corrected import for Grade model
from models.schedules import Schedule      # Corrected import for Schedule model

class AbstractRole(ABC):
    """
    Abstract base class for all user roles in the EduPlatform.
    Defines common attributes and abstract methods that must be implemented by subclasses.
    """
    _next_id = 1 # Class-level attribute to generate unique IDs for users

    def __init__(self, full_name: str, email: str, password: str):
        """
        Initializes an AbstractRole instance.
        Attributes:
        _id: Unique ID (int)
        _full_name: Full name (str)
        _email: Electronic mail (str)
        _password_hash: Hashed password (str)
        _created_at: Registration date (str, ISO format)
        """
        self._id = AbstractRole._next_id
        AbstractRole._next_id += 1
        self._full_name = full_name
        self._email = email
        self._password_hash = self._hash_password(password) # Hash the password for security
        self._created_at = datetime.datetime.now().isoformat() # Current timestamp in ISO format

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hashes the password using SHA256 for basic security.
        """
        return hashlib.sha256(password.encode()).hexdigest()

    @property
    def id(self) -> int:
        """Returns the unique ID of the user."""
        return self._id

    @property
    def full_name(self) -> str:
        """Returns the full name of the user."""
        return self._full_name

    @property
    def email(self) -> str:
        """Returns the email address of the user."""
        return self._email

    @property
    def created_at(self) -> str:
        """Returns the creation timestamp of the user account."""
        return self._created_at

    @abstractmethod
    def get_profile(self) -> dict:
        """
        Abstract method: Returns the user's profile information.
        Must be implemented by subclasses.
        """
        pass

    @abstractmethod
    def update_profile(self, **kwargs):
        """
        Abstract method: Updates the user's profile information.
        Must be implemented by subclasses.
        """
        pass

class User(AbstractRole):
    """
    Base user class inheriting from AbstractRole.
    Adds common user functionalities like notifications and authentication.
    """
    def __init__(self, full_name: str, email: str, password: str, role: UserRole):
        """
        Initializes a User instance.
        Attributes:
        role: User role (enum: Admin, Teacher, Student, Parent)
        _notifications: List of notifications (list)
        phone: Additional profile information (str, optional)
        address: Additional profile information (str, optional)
        """
        super().__init__(full_name, email, password)
        self.role = role
        self._notifications = [] # List to store Notification objects
        self.phone = None # Additional profile information
        self.address = None # Additional profile information

    def get_profile(self) -> dict:
        """
        Returns the user's profile information, including role, phone, address, and notifications.
        Converts lists/dicts to JSON strings for export compatibility.
        """
        profile = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role.value,
            "created_at": self.created_at,
            "phone": self.phone if self.phone is not None else "", # Handle None values for export
            "address": self.address if self.address is not None else "", # Handle None values for export
            # Convert list of Notification objects' info to a JSON string
            "notifications": json.dumps([n.get_notification_info() for n in self._notifications])
        }
        return profile

    def update_profile(self, **kwargs):
        """
        Updates the user's profile attributes.
        Allowed updates: full_name, email, password, phone, address.
        """
        if 'full_name' in kwargs:
            self._full_name = kwargs['full_name']
        if 'email' in kwargs:
            self._email = kwargs['email']
        if 'password' in kwargs:
            self._password_hash = self._hash_password(kwargs['password'])
        if 'phone' in kwargs:
            self.phone = kwargs['phone']
        if 'address' in kwargs:
            self.address = kwargs['address']

    def add_notification(self, message: str, priority: str = "normal"):
        """
        Adds a new notification to the user's list.
        """
        notification = Notification(message, self.id, priority=priority)
        self._notifications.append(notification)

    def view_notifications(self, filter_read: bool = False, filter_priority: str = None) -> list:
        """
        Views notifications, with optional filters for read status and priority.
        Returns a list of notification information.
        """
        filtered_notifications = []
        for notif in self._notifications:
            if filter_read and notif.is_read:
                continue
            if filter_priority and notif.priority.lower() != filter_priority.lower():
                continue
            filtered_notifications.append(notif.get_notification_info())
        return filtered_notifications

    def delete_notification(self, notification_id: int) -> bool:
        """
        Deletes a notification by its ID.
        Returns True if the notification was found and deleted, False otherwise.
        """
        original_len = len(self._notifications)
        self._notifications = [n for n in self._notifications if n.id != notification_id]
        return len(self._notifications) < original_len

    def authenticate(self, password: str) -> bool:
        """
        Authenticates the user by checking the provided password against the stored hash.
        Returns True if authentication is successful, False otherwise.
        """
        return self._hash_password(password) == self._password_hash

class Student(User):
    """
    Represents a student in the EduPlatform, inheriting from User.
    Handles student-specific data like grades, subjects, and assignments.
    """
    def __init__(self, full_name: str, email: str, password: str, grade_level: str):
        """
        Initializes a Student instance.
        Attributes:
        grade: Class/grade level (e.g., "9-A")
        subjects: Subjects student is taking (dict: {subject_name: teacher_id})
        assignments: Student's assignments (dict: {assignment_id: status})
        grades: Student's grades (dict: {subject: [grade1, grade2, ...]})
        """
        super().__init__(full_name, email, password, UserRole.STUDENT)
        self.grade = grade_level # e.g., "9-A"
        self.subjects = {} # {subject_name: teacher_id}
        self.assignments = {} # {assignment_id: status}
        self.grades = {} # {subject: [grade1, grade2, ...]}

    def get_profile(self) -> dict:
        """
        Overrides User.get_profile to include student-specific details.
        Converts lists/dicts to JSON strings for export compatibility.
        """
        profile = super().get_profile()
        profile.update({
            "grade_level": self.grade,
            # Convert dictionaries to JSON strings
            "subjects_enrolled": json.dumps(self.subjects),
            "current_assignments_status": json.dumps(self.assignments),
            "all_grades": json.dumps(self.grades)
        })
        return profile

    def update_profile(self, **kwargs):
        """
        Updates the student's profile information.
        Allows updating base User attributes and student-specific 'grade'.
        """
        super().update_profile(**kwargs)
        if 'grade_level' in kwargs:
            self.grade = kwargs['grade_level']

    def submit_assignment(self, assignment_id: int, content: str, all_assignments: dict) -> bool:
        """
        Submits an assignment.
        Checks for deadline and content length restrictions.
        Returns True if submission is successful, False otherwise.
        """
        # Ensure Assignment is correctly imported from models.assignments
        # (This is already handled at the top of the file)
        
        assignment: Assignment = all_assignments.get(assignment_id)
        if not assignment:
            print(f"Error: Assignment with ID {assignment_id} not found.")
            return False

        # --- CORRECTED DEADLINE COMPARISON ---
        # self.deadline in Assignment is a datetime.date object.
        # Compare dates directly.
        today = datetime.date.today()
        is_late = today > assignment.deadline

        if is_late:
            print(f"Error: Assignment {assignment_id} deadline has passed. Submission marked as late.")
            assignment.add_submission(self.id, content, is_late=True)
            self.assignments[assignment_id] = AssignmentStatus.LATE_SUBMISSION.value
            return False # Return False as it was a late submission, not an "on-time success"

        # Check content length restriction (e.g., max 500 characters)
        if len(content) > 500:
            print(f"Error: Assignment content exceeds 500 characters. Current length: {len(content)}")
            return False
            
        assignment.add_submission(self.id, content) # Add submission to the assignment
        self.assignments[assignment_id] = AssignmentStatus.SUBMITTED.value # Update student's assignment status
        print(f"Assignment {assignment_id} submitted successfully by {self.full_name}.")
        return True

    def view_grades(self, subject: str = None) -> dict:
        """
        Views grades, optionally filtered by subject.
        Returns a dictionary of grades.
        """
        if subject:
            if subject in self.grades:
                return {subject: self.grades[subject]}
            else:
                print(f"No grades found for subject: {subject}")
                return {}
        return self.grades

    def calculate_average_grade(self, subject: str = None) -> float:
        """
        Calculates the average grade for a student, optionally by subject.
        Returns the average grade as a float.
        """
        grades_to_avg = []
        if subject:
            if subject in self.grades:
                grades_to_avg.extend(self.grades[subject])
        else:
            for sub_grades in self.grades.values():
                grades_to_avg.extend(sub_grades)

        if not grades_to_avg:
            return 0.0 # No grades to calculate

        return sum(grades_to_avg) / len(grades_to_avg)

class Teacher(User):
    """
    Represents a teacher in the EduPlatform, inheriting from User.
    Handles teacher-specific data like subjects taught, classes, and assignments given.
    """
    def __init__(self, full_name: str, email: str, password: str):
        """
        Initializes a Teacher instance.
        Attributes:
        subjects: Subjects taught (list of str)
        classes: Classes taught (list of str)
        assignments: Assignments given (dict: {assignment_id: Assignment object})
        """
        super().__init__(full_name, email, password, UserRole.TEACHER)
        self.subjects = [] # List of subjects taught
        self.classes = [] # List of class IDs taught
        self.assignments = {} # {assignment_id: Assignment object}
        self.workload = 0 # Teaching hours/workload

    def get_profile(self) -> dict:
        """
        Overrides User.get_profile to include teacher-specific details.
        Converts lists/dicts to JSON strings for export compatibility.
        """
        profile = super().get_profile()
        profile.update({
            # Convert lists to JSON strings
            "subjects_taught": json.dumps(self.subjects),
            "classes_taught": json.dumps(self.classes),
            # Convert list of assignment info dictionaries to a JSON string
            "assignments_created": json.dumps([a.get_assignment_info() for a in self.assignments.values()]),
            "workload": self.workload
        })
        return profile

    def update_profile(self, **kwargs):
        """
        Updates the teacher's profile information.
        Allows updating base User attributes and teacher-specific 'subjects' or 'classes'.
        """
        super().update_profile(**kwargs)
        if 'subjects' in kwargs and isinstance(kwargs['subjects'], list):
            self.subjects = list(set(self.subjects + kwargs['subjects'])) # Add new subjects, avoid duplicates
        if 'classes' in kwargs and isinstance(kwargs['classes'], list):
            self.classes = list(set(self.classes + kwargs['classes'])) # Add new classes, avoid duplicates
        if 'workload' in kwargs and isinstance(kwargs['workload'], (int, float)):
            self.workload = kwargs['workload']

    def create_assignment(self, title: str, description: str, deadline: str, subject: str,
                            class_id: str, difficulty: AssignmentDifficulty, all_assignments: dict) -> 'Assignment':
        """
        Creates a new assignment and adds it to the teacher's assignments.
        Also adds it to a global assignments list (passed as all_assignments for now).
        """
        # Ensure Assignment is correctly imported from models.assignments
        # (This is already handled at the top of the file)
        
        new_assignment = Assignment(
            self.id,          # teacher_id (Corrected position)
            title,
            description,
            deadline,
            subject,          # subject (Corrected position)
            class_id,
            difficulty
        )
        self.assignments[new_assignment.id] = new_assignment # Add to teacher's assignments
        all_assignments[new_assignment.id] = new_assignment # Add to global assignments list
        print(f"Assignment '{title}' created by {self.full_name} for {class_id}.")
        return new_assignment

    def grade_assignment(self, assignment_id: int, student_id: int, grade_value: int,
                            all_assignments: dict, all_students: dict) -> bool:
        """
        Grades a student's submission for a given assignment.
        Updates the assignment's grades and the student's grades.
        """
        # Ensure Assignment and Grade are correctly imported from their respective models
        # (This is already handled at the top of the file)
        
        assignment: Assignment = all_assignments.get(assignment_id)
        student: Student = all_students.get(student_id)

        if not assignment:
            print(f"Error: Assignment with ID {assignment_id} not found.")
            return False
        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return False
        if student_id not in assignment.submissions:
            print(f"Error: Student {student.full_name} has not submitted this assignment.")
            return False
        if not (1 <= grade_value <= 5):
            print("Error: Grade value must be between 1 and 5.")
            return False
            
        # Set grade in Assignment object
        assignment.set_grade(student_id, grade_value) # Sets grade and updates status in assignment

        # Add or update grade in student's grades list
        if assignment.subject not in student.grades:
            student.grades[assignment.subject] = []
        
        # Simple check to prevent adding the exact same grade value multiple times for the same subject
        if grade_value not in student.grades[assignment.subject]:
             student.grades[assignment.subject].append(grade_value)

        # Create a Grade object (from models/grades.py)
        new_grade = Grade(student_id, assignment_id, assignment.subject, grade_value, self.id)
        # In a real system, `new_grade` would typically be stored in a central grades collection/dictionary
        # For example, if you have a `platform.grades` dict in your EduPlatform class.

        print(f"Assignment {assignment_id} for student {student.full_name} graded: {grade_value}")
        return True

    def view_student_progress(self, student_id: int, all_students: dict) -> dict:
        """
        Views a specific student's progress by their ID.
        Returns a dictionary summarizing student's grades and assignments.
        """
        student: Student = all_students.get(student_id)
        if not student:
            print(f"Error: Student with ID {student_id} not found.")
            return {}

        progress_report = {
            "student_full_name": student.full_name,
            "student_grade_level": student.grade,
            "grades_by_subject": student.view_grades(),
            "assignment_statuses": student.assignments,
            "average_grade_overall": student.calculate_average_grade()
        }
        print(f"Progress report for {student.full_name}:")
        for key, value in progress_report.items():
            print(f"  {key}: {value}")
        return progress_report

class Parent(User):
    """
    Represents a parent in the EduPlatform, inheriting from User.
    Allows parents to monitor their children's academic progress.
    """
    def __init__(self, full_name: str, email: str, password: str, children_ids: list[int] = None):
        """
        Initializes a Parent instance.
        Attributes:
        children: List of Student IDs of their children (list of int)
        notification_preferences: Preferences for child-related notifications (dict)
        """
        super().__init__(full_name, email, password, UserRole.PARENT)
        self.children = children_ids if children_ids is not None else [] # List of student IDs
        self.notification_preferences = {"low_grade_alert": True} # Default preferences

    def get_profile(self) -> dict:
        """
        Overrides User.get_profile to include parent-specific details.
        Converts lists/dicts to JSON strings for export compatibility.
        """
        profile = super().get_profile()
        profile.update({
            # Convert lists/dicts to JSON strings
            "children_ids": json.dumps(self.children),
            "notification_preferences": json.dumps(self.notification_preferences)
        })
        return profile

    def update_profile(self, **kwargs):
        """
        Updates the parent's profile information.
        Allows updating base User attributes and parent-specific 'notification_preferences'.
        """
        super().update_profile(**kwargs)
        if 'children' in kwargs and isinstance(kwargs['children'], list):
            self.children = list(set(self.children + kwargs['children']))
        if 'notification_preferences' in kwargs and isinstance(kwargs['notification_preferences'], dict):
            self.notification_preferences.update(kwargs['notification_preferences'])

    def view_child_grades(self, child_id: int, all_students: dict) -> dict:
        """
        Views a specific child's grades.
        Returns the child's grades dictionary.
        """
        if child_id not in self.children:
            print(f"Error: Child with ID {child_id} is not registered as your child.")
            return {}
        
        child: Student = all_students.get(child_id)
        if not child:
            print(f"Error: Child with ID {child_id} not found in the system.")
            return {}
        
        return child.view_grades()

    def view_child_assignments(self, child_id: int, all_students: dict) -> dict:
        """
        Views a specific child's assignments and their statuses.
        Returns the child's assignments dictionary.
        """
        if child_id not in self.children:
            print(f"Error: Child with ID {child_id} is not registered as your child.")
            return {}
        
        child: Student = all_students.get(child_id)
        if not child:
            print(f"Error: Child with ID {child_id} not found in the system.")
            return {}
        
        return child.assignments

    def receive_child_notification(self, child_id: int, message: str, priority: str = "normal"):
        """
        Allows parents to receive special notifications related to their child.
        """
        if child_id in self.children:
            self.add_notification(f"Regarding child {child_id}: {message}", priority=priority)
            print(f"Parent {self.full_name} received notification about child {child_id}.")
        else:
            print(f"Error: Child with ID {child_id} is not associated with this parent.")

class Admin(User):
    """
    Represents an administrator in the EduPlatform, inheriting from User.
    Has system-level control, including user management and report generation.
    """
    def __init__(self, full_name: str, email: str, password: str):
        """
        Initializes an Admin instance.
        Attributes:
        permissions: List of permissions (list of str)
        """
        super().__init__(full_name, email, password, UserRole.ADMIN)
        self.permissions = ["manage_users", "generate_reports", "system_settings"] # Default permissions

    def get_profile(self) -> dict:
        """
        Overrides User.get_profile to include admin-specific details.
        Converts lists/dicts to JSON strings for export compatibility.
        """
        profile = super().get_profile()
        profile.update({
            # Convert list to JSON string
            "permissions": json.dumps(self.permissions)
        })
        return profile

    def update_profile(self, **kwargs):
        """
        Updates the admin's profile information.
        Allows updating base User attributes and adding 'permissions'.
        """
        super().update_profile(**kwargs)
        if 'permissions' in kwargs and isinstance(kwargs['permissions'], list):
            self.permissions = list(set(self.permissions + kwargs['permissions'])) # Add new permissions, avoid duplicates

    def add_user(self, user_data: dict, all_users: dict) -> User:
        """
        Adds a new user to the system based on provided user data.
        Returns the created User object.
        """
        # Specific imports for type checking within this method
        from models.users import Student, Teacher, Parent, Admin # Ensure these are imported relative to models.users
        
        role_str = user_data.get("role", "").lower()
        full_name = user_data.get("full_name")
        email = user_data.get("email")
        password = user_data.get("password")

        if not all([full_name, email, password, role_str]):
            print("Error: Missing required user data (full_name, email, password, role).")
            return None

        new_user = None
        if role_str == UserRole.STUDENT.value.lower():
            grade_level = user_data.get("grade_level")
            if not grade_level:
                print("Error: Student requires 'grade_level'.")
                return None
            new_user = Student(full_name, email, password, grade_level)
        elif role_str == UserRole.TEACHER.value.lower():
            new_user = Teacher(full_name, email, password)
        elif role_str == UserRole.PARENT.value.lower():
            # Pass children_ids if provided in user_data
            children_ids = user_data.get("children_ids")
            new_user = Parent(full_name, email, password, children_ids=children_ids)
        elif role_str == UserRole.ADMIN.value.lower():
            new_user = Admin(full_name, email, password)
        else:
            print(f"Error: Invalid user role '{role_str}'.")
            return None

        if new_user:
            all_users[new_user.id] = new_user # Add to the global users dictionary
            print(f"User '{new_user.full_name}' with role {new_user.role.value} added.")
            return new_user
        return None

    def remove_user(self, user_id: int, all_users: dict) -> bool:
        """
        Removes a user from the system by their ID.
        Returns True if the user was removed, False otherwise.
        """
        if user_id in all_users:
            # Additional logic might be needed here to remove associated data (assignments, grades etc.)
            del all_users[user_id]
            print(f"User with ID {user_id} removed.")
            return True
        print(f"Error: User with ID {user_id} not found.")
        return False

    def generate_report(self, report_type: str, all_data: dict) -> dict:
        """
        Generates various system reports.
        Report types: "student_success", "teacher_workload", "class_statistics".
        """
        report_data = {}
        if report_type == "student_success":
            report_data["student_success"] = {}
            for user_id, user in all_data['users'].items():
                if isinstance(user, Student):
                    report_data["student_success"][user.full_name] = {
                        "average_overall_grade": user.calculate_average_grade(),
                        # For reports, it's fine to keep this as a dict for analysis within Python
                        # If this report itself is exported to Excel, then you'd JSON-serialize again.
                        "grades_by_subject": user.view_grades()
                    }
            print("Student success report generated.")
        elif report_type == "teacher_workload":
            report_data["teacher_workload"] = {}
            for user_id, user in all_data['users'].items():
                if isinstance(user, Teacher):
                    report_data["teacher_workload"][user.full_name] = {
                        "subjects_taught_count": len(user.subjects),
                        "classes_taught_count": len(user.classes),
                        "assignments_created_count": len(user.assignments),
                        "current_workload_hours": user.workload
                    }
            print("Teacher workload report generated.")
        elif report_type == "class_statistics":
            class_stats = {}
            for user_id, user in all_data['users'].items():
                if isinstance(user, Student):
                    if user.grade not in class_stats:
                        class_stats[user.grade] = {"total_students": 0, "total_avg_grade": 0, "students_data": []}
                    
                    class_stats[user.grade]["total_students"] += 1
                    avg_grade = user.calculate_average_grade()
                    class_stats[user.grade]["total_avg_grade"] += avg_grade
                    class_stats[user.grade]["students_data"].append({
                        "id": user.id, "name": user.full_name, "avg_grade": avg_grade
                    })
            
            for grade, stats in class_stats.items():
                if stats["total_students"] > 0:
                    stats["average_class_grade"] = stats["total_avg_grade"] / stats["total_students"]
                else:
                    stats["average_class_grade"] = 0
                del stats["total_avg_grade"]
            
            report_data["class_statistics"] = class_stats
            print("Class statistics report generated.")
        else:
            print(f"Error: Unknown report type '{report_type}'.")
            return {}
        
        return report_data