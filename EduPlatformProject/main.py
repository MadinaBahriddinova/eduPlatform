from EduPlatform.edu_platform import EduPlatform
from core.enums import UserRole, AssignmentDifficulty
import datetime # Just for example date input

def run_edu_platform():
    platform = EduPlatform()

    # --- 1. Admin Login (Initial) ---
    print("\n--- Initial Admin Login ---")
    admin_user = platform.authenticate_user("admin@eduplatform.com", "adminpass")
    if not admin_user:
        print("Failed to authenticate initial admin. Exiting.")
        return

    # --- 2. Registering Users (Admin function) ---
    print("\n--- Registering Users ---")
    student1 = platform.register_user("Ali Valiyev", "ali@student.com", "pass123", UserRole.STUDENT, grade_level="9-A")
    student2 = platform.register_user("Dilnoza Karimova", "dilnoza@student.com", "pass123", UserRole.STUDENT, grade_level="9-A")
    teacher1 = platform.register_user("Sarvar Saidov", "sarvar@teacher.com", "teachpass", UserRole.TEACHER)
    parent1 = platform.register_user("Gulnora Aliyeva", "gulnora@parent.com", "parentpass", UserRole.PARENT, children_ids=[student1.id])

    # Try to register with duplicate email
    platform.register_user("Ali Duplicate", "ali@student.com", "anotherpass", UserRole.STUDENT, grade_level="10-B")

    # --- 3. Update User Profiles ---
    print("\n--- Updating User Profiles ---")
    if student1:
        student1.update_profile(phone="998901234567", address="Tashkent, Chilonzor")
        print(f"Updated profile for {student1.full_name}: {student1.get_profile()['phone']}")
    
    if teacher1:
        teacher1.update_profile(subjects=["Math", "Physics"], classes=["9-A", "10-B"])
        print(f"Teacher {teacher1.full_name} subjects: {teacher1.subjects}")

    # In main.py, locate the section where "Late Homework" is created:

# --- Teacher Creates Assignment (for "Late Homework") ---
# The deadline needs to be in 'YYYY-MM-DD' format.
# datetime.datetime.now().isoformat() produces 'YYYY-MM-DDTHH:MM:SS.ffffff'
# We need to split it to get just the date part.

# Current time is Saturday, June 14, 2025 at 10:50:15 PM +05.
# Let's set a deadline that is in the past for "Late Homework"
# and a future one for "Algebra Worksheet" if it's not already.


# ... (previous code in main.py) ...

    print("\n--- Teacher Creates Assignment ---")
    if teacher1 and student1 and parent1:
    # Fix for "Algebra Worksheet" deadline: Ensure it's 'YYYY-MM-DD'
    # It seems this one might already be implicitly working or was fixed,
    # but let's make it explicit and robust.
        future_date_str = (datetime.date.today() + datetime.timedelta(days=7)).isoformat() # A week from now
        assignment1 = platform.create_assignment(
            teacher1.id, "Algebra Worksheet", "Complete exercises 1-10", future_date_str, # Use the correct date string
            "Math", "9-A", AssignmentDifficulty.MEDIUM
        )
        if assignment1:
            print(f"Assignment created: {assignment1.title}")

# ... (student submission for assignment1) ...

# --- NEW ASSIGNMENT CREATION (Late Homework) ---
# This is the line causing the specific TypeError.
# The deadline for 'Late Homework' should be in the past and in 'YYYY-MM-DD' format.
    past_date = datetime.date.today() - datetime.timedelta(days=1) # Yesterday's date
    past_date_str = past_date.isoformat() # This directly gives YYYY-MM-DD

    late_assignment = platform.create_assignment(
        teacher1.id, "Late Homework", "Write an essay on World War II", past_date_str, # <--- Fix this line
        "History", "9-A", AssignmentDifficulty.HARD
    )
    if late_assignment:
        print(f"Assignment '{late_assignment.title}' created by {teacher1.full_name} for {late_assignment.class_id}.")

# ... (rest of your main.py) ...

    # --- 5. Student Submits Assignment ---
    print("\n--- Student Submits Assignment ---")
    if student1 and assignment1:
        platform.submit_assignment(student1.id, assignment1.id, "My completed algebra work.")
        # Try a late submission
        past_deadline = (datetime.datetime.now() - datetime.timedelta(days=1)).isoformat()
        late_assignment = platform.create_assignment(
            teacher1.id, "Late Homework", "This was due yesterday", past_deadline,
            "History", "9-A", AssignmentDifficulty.EASY
        )
        if late_assignment and student2:
             platform.submit_assignment(student2.id, late_assignment.id, "My very late history essay.")


    # --- 6. Teacher Grades Assignment ---
    print("\n--- Teacher Grades Assignment ---")
    if teacher1 and student1 and assignment1:
        platform.grade_assignment(teacher1.id, student1.id, assignment1.id, 4, "Good effort!")
        # Trigger low grade notification to parent
        platform.grade_assignment(teacher1.id, student1.id, assignment1.id, 2, "Needs more practice.") # Simulates a low grade


    # --- 7. View Grades and Notifications ---
    print("\n--- Viewing Grades and Notifications ---")
    if student1:
        print(f"\n{student1.full_name}'s Grades: {student1.view_grades()}")
        print(f"{student1.full_name}'s Notifications: {student1.view_notifications()}")
        print(f"Average grade for {student1.full_name}: {student1.calculate_average_grade()}")

    if parent1 and student1:
        print(f"\n{parent1.full_name}'s view of {student1.full_name}'s grades: {parent1.view_child_grades(student1.id, platform.users)}")
        print(f"{parent1.full_name}'s notifications: {parent1.view_notifications()}")
    
    # --- 8. Schedule Management ---
    print("\n--- Schedule Management ---")
    schedule9A_mon = platform.create_schedule("9-A", "Monday")
    if schedule9A_mon:
        platform.add_lesson_to_schedule(schedule9A_mon.id, "09:00", "Math", teacher1.id)
        platform.add_lesson_to_schedule(schedule9A_mon.id, "10:00", "Physics", teacher1.id)
        print(f"Schedule for {schedule9A_mon.class_id} on {schedule9A_mon.day}: {schedule9A_mon.view_schedule()['lessons']}")
        
        # Try adding lesson with conflicting teacher time
        platform.add_lesson_to_schedule(schedule9A_mon.id, "09:00", "Chemistry", teacher1.id) # Should fail due to conflict

    # --- 9. Admin Generates Reports ---
    print("\n--- Admin Generating Reports ---")
    if admin_user:
        student_report = platform.generate_report(admin_user.id, "student_success")
        teacher_report = platform.generate_report(admin_user.id, "teacher_workload")
        class_report = platform.generate_report(admin_user.id, "class_statistics")
        
        # Print a snippet of a report
        print("\nStudent Success Report Snippet:")
        for student_name, data in list(student_report.get("student_success", {}).items())[:2]:
            print(f"- {student_name}: Avg Grade {data['average_overall_grade']:.2f}")

    # --- 10. Manual Export (already happens automatically on change) ---
    print("\n--- Manual Export Check ---")
    # platform.export_to_xlsx("final_eduplatform_data.xlsx")
    # platform.export_to_csv("final_eduplatform_data")
    # platform.export_to_sql("final_eduplatform_data.sql")
    platform.view_export_log()

    # --- 11. Remove User ---
    print("\n--- Saving Export Log ---")
    platform.save_export_log()
    print("--- Program Finished Successfully---")


if __name__ == "__main__":
    run_edu_platform()