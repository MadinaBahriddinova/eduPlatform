from __future__ import annotations
import datetime

class Schedule:
    """
    Represents a class schedule for a specific class/group on a given day.
    """
    _next_id = 1 # Class-level attribute to generate unique IDs for schedules

    def __init__(self, class_id: str, day: str):
        """
        Initializes a Schedule instance.
        Attributes:
        id: Unique schedule ID (int)
        class_id: The ID of the class/group this schedule is for (str)
        day: Day of the week (e.g., "Monday", "Tuesday") (str)
        lessons: Dictionary of lessons for the day ({time: {'subject': str, 'teacher_id': int}})
        """
        self._id = Schedule._next_id
        Schedule._next_id += 1
        self.class_id = class_id
        self.day = day
        # Lessons: { "09:00": {"subject": "Math", "teacher_id": 1}, "10:00": {...} }
        self.lessons = {}

    @property
    def id(self) -> int:
        return self._id

    def add_lesson(self, time: str, subject: str, teacher_id: int) -> bool:
        """
        Adds a lesson to the schedule for a specific time.
        Checks for time conflicts within this schedule.
        Time format: "HH:MM" (e.g., "09:00")
        """
        # Basic time format validation (can be more robust)
        try:
            datetime.datetime.strptime(time, "%H:%M").time()
        except ValueError:
            print(f"Error: Invalid time format '{time}'. Use HH:MM (e.g., 09:00).")
            return False

        if time in self.lessons:
            print(f"Error: A lesson is already scheduled at {time} on {self.day} for class {self.class_id}.")
            return False
        
        self.lessons[time] = {"subject": subject, "teacher_id": teacher_id}
        print(f"Lesson '{subject}' added for {self.class_id} on {self.day} at {time}.")
        return True

    def view_schedule(self) -> dict:
        """Returns the daily schedule."""
        return {
            "schedule_id": self.id,
            "class_id": self.class_id,
            "day": self.day,
            "lessons": self.lessons
        }

    def remove_lesson(self, time: str) -> bool:
        """
        Removes a lesson from the schedule at a specific time.
        """
        if time in self.lessons:
            del self.lessons[time]
            print(f"Lesson at {time} removed from schedule for {self.class_id} on {self.day}.")
            return True
        print(f"Error: No lesson found at {time} to remove.")
        return False