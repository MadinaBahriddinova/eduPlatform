from __future__ import annotations 

import hashlib
import datetime
from abc import ABC, abstractmethod
from enums import UserRole
from enums import UserRole, AssignmentDifficulty, AssignmentStatus
from notifications import Notification 
from assignments import Assignment   # <--- ADD THIS LINE
from grades import Grade              # <--- ADD THIS LINE
from schedules import Schedule 

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
        This uses a simple hash function. 
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

    # ... (Previous code for AbstractRole) ...

# Import Notification class (will be defined later in notifications.py)
# For now, we'll assume it exists or use a forward declaration if needed.
# Let's put a placeholder for now and properly import later.
# from notifications import Notification # This will be uncommented once Notification is defined

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
        """Returns the user's profile information, including role, phone, address, and notifications. """
        profile = {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role.value,
            "created_at": self.created_at,
            "phone": self.phone, # Added phone 
            "address": self.address, # Added address 
            # Notifications will be added here once the Notification class is defined
            "notifications": [n.get_notification_info() for n in self._notifications]
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
        if 'password' in kwargs: # Password update will re-hash the new password
            self._password_hash = self._hash_password(kwargs['password'])
        if 'phone' in kwargs:
            self.phone = kwargs['phone'] # Update phone 
        if 'address' in kwargs:
            self.address = kwargs['address'] # Update address 

    def add_notification(self, message: str, priority: str = "normal"):
        """
        Adds a new notification to the user's list. 
        Priority can be used for filtering.
        """
        # We need a Notification class to instantiate here.
        # For now, we'll add a simple dictionary, but will replace with Notification object later.
        # This is a temporary placeholder.
        from notifications import Notification # Import Notification class here to avoid circular dependency for now
        notification = Notification(message, self.id, priority=priority)
        self._notifications.append(notification)


    def view_notifications(self, filter_read: bool = False, filter_priority: str = None) -> list:
        """
        Views notifications, with optional filters for read status and priority. 
        Returns a list of notification information.
        """
        filtered_notifications = []
        for notif in self._notifications:
            if filter_read and notif.is_read: # Filter by read status 
                continue
            if filter_priority and notif.priority.lower() != filter_priority.lower(): # Filter by priority 
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
    

# ... (Previous code for AbstractRole and User) ...

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
        """
        profile = super().get_profile()
        profile.update({
            "grade_level": self.grade,
            "subjects_enrolled": self.subjects,
            "current_assignments_status": self.assignments,
            "all_grades": self.grades
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
        # Assume all_assignments is a global or passed-in dictionary of all Assignment objects
        # To avoid circular imports, we might pass it as a parameter for now.
        from assignments import Assignment # Temporary import to avoid circular dependency
        
        assignment: Assignment = all_assignments.get(assignment_id)
        if not assignment:
            print(f"Error: Assignment with ID {assignment_id} not found.")
            return False

        # Check for deadline 
        deadline_dt = datetime.datetime.fromisoformat(assignment.deadline)
        if datetime.datetime.now() > deadline_dt:
            print(f"Error: Assignment {assignment_id} deadline has passed. Submission marked as late.")
            assignment.add_submission(self.id, content, is_late=True)
            self.assignments[assignment_id] = AssignmentStatus.LATE_SUBMISSION.value
            return False

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
    

    # ... (Previous code for AbstractRole, User, Student) ...


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
        """
        profile = super().get_profile()
        profile.update({
            "subjects_taught": self.subjects,
            "classes_taught": self.classes,
            "assignments_created": [a.get_assignment_info() for a in self.assignments.values()],
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
        from assignments import Assignment # Temporary import to avoid circular dependency
        
        new_assignment = Assignment(
            title, description, deadline, subject, self.id, class_id, difficulty
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
        from assignments import Assignment # Temporary import
        from grades import Grade # Temporary import

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
        
        # Prevent duplicate grades for the same assignment if re-grading (simple check)
        # In a more complex system, grades would be objects with unique IDs or linked to assignment_id
        if grade_value not in student.grades[assignment.subject]: # Simple check
             student.grades[assignment.subject].append(grade_value)

        # Create a Grade object (from grades.py)
        new_grade = Grade(student_id, assignment.subject, grade_value, self.id)
        
        # In a real system, this new_grade would be stored globally.
        # For this in-memory system, we can pass it to a central data manager.
        # For now, we'll just print it.
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
    

    # ... (Previous code for AbstractRole, User, Student, Teacher) ...

class Parent(User):
    """
    Represents a parent in the EduPlatform, inheriting from User.
    Allows parents to monitor their children's academic progress.
    """
    def __init__(self, full_name: str, email: str, password: str):
        """
        Initializes a Parent instance.
        Attributes:
        children: List of Student IDs of their children (list of int) 
        notification_preferences: Preferences for child-related notifications (dict) 
        """
        super().__init__(full_name, email, password, UserRole.PARENT)
        self.children = [] # List of student IDs 
        self.notification_preferences = {"low_grade_alert": True} # Default preferences 

    def get_profile(self) -> dict:
        """
        Overrides User.get_profile to include parent-specific details.
        """
        profile = super().get_profile()
        profile.update({
            "children_ids": self.children,
            "notification_preferences": self.notification_preferences
        })
        return profile

    def update_profile(self, **kwargs):
        """
        Updates the parent's profile information.
        Allows updating base User attributes and parent-specific 'notification_preferences'.
        """
        super().update_profile(**kwargs)
        if 'children' in kwargs and isinstance(kwargs['children'], list):
            # You might want more sophisticated logic here (e.g., adding only valid student IDs)
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
        For example, if the child's grade is low. 
        """
        if child_id in self.children:
            self.add_notification(f"Regarding child {child_id}: {message}", priority=priority)
            print(f"Parent {self.full_name} received notification about child {child_id}.")
        else:
            print(f"Error: Child with ID {child_id} is not associated with this parent.")



            # ... (Previous code for AbstractRole, User, Student, Teacher, Parent) ...

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
        """
        profile = super().get_profile()
        profile.update({
            "permissions": self.permissions
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
        from users import Student, Teacher, Parent # Import specific classes for type checking
        
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
            new_user = Parent(full_name, email, password)
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
            # Example: student success graph by subject 
            report_data["student_success"] = {}
            for user_id, user in all_data['users'].items():
                if isinstance(user, Student):
                    report_data["student_success"][user.full_name] = {
                        "average_overall_grade": user.calculate_average_grade(),
                        "grades_by_subject": user.view_grades()
                    }
            print("Student success report generated.")
        elif report_type == "teacher_workload":
            # Example: teacher workload analysis 
            report_data["teacher_workload"] = {}
            for user_id, user in all_data['users'].items():
                if isinstance(user, Teacher):
                    report_data["teacher_workload"][user.full_name] = {
                        "subjects_taught_count": len(user.subjects),
                        "classes_taught_count": len(user.classes),
                        "assignments_created_count": len(user.assignments),
                        "current_workload_hours": user.workload # From Teacher attribute 
                    }
            print("Teacher workload report generated.")
        elif report_type == "class_statistics":
            # Example: general class statistics 
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
            
            # Calculate overall average for each class
            for grade, stats in class_stats.items():
                if stats["total_students"] > 0:
                    stats["average_class_grade"] = stats["total_avg_grade"] / stats["total_students"]
                else:
                    stats["average_class_grade"] = 0
                del stats["total_avg_grade"] # Remove intermediate sum
            
            report_data["class_statistics"] = class_stats
            print("Class statistics report generated.")
        else:
            print(f"Error: Unknown report type '{report_type}'.")
            return {}
        
        return report_data
    

