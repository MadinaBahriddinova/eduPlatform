import datetime

class Notification:
    """
    Represents a notification in the EduPlatform.
    Notifications can be sent to any user. 
    """
    _next_id = 1 # Class-level attribute to generate unique IDs for notifications

    def __init__(self, message: str, recipient_id: int, priority: str = "normal"):
        """
        Initializes a Notification instance.
        Attributes:
        id: Notification ID (int) 
        message: Message text (str) 
        recipient_id: Recipient ID (int) 
        created_at: Creation date (str) 
        is_read: Status indicating if the notification has been read (bool)
        priority: Priority of the notification (str, e.g., "normal", "important") 
        """
        self._id = Notification._next_id
        Notification._next_id += 1
        self.message = message
        self.recipient_id = recipient_id
        self.created_at = datetime.datetime.now().isoformat()
        self.is_read = False # Default to unread
        self.priority = priority.lower() # Store priority in lowercase for consistency 

    @property
    def id(self) -> int:
        return self._id

    def send(self):
        """
        Simulates sending a notification.
        In a real system, this would involve pushing to a UI or external service.
        For now, it prints a message.
        """
        print(f"Notification {self.id} sent to user {self.recipient_id}: '{self.message}'")

    def mark_as_read(self):
        """Marks the notification as read. """
        self.is_read = True

    def get_notification_info(self) -> dict:
        """Returns a dictionary with notification details."""
        return {
            "id": self.id,
            "message": self.message,
            "recipient_id": self.recipient_id,
            "created_at": self.created_at,
            "is_read": self.is_read,
            "priority": self.priority
        }