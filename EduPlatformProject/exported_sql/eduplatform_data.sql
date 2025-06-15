CREATE TABLE [tbl_user] (
    [id] INT PRIMARY KEY,
    [full_name] NVARCHAR(255),
    [email] NVARCHAR(255),
    [role] NVARCHAR(255),
    [created_at] NVARCHAR(255),
    [phone] NVARCHAR(255),
    [address] NVARCHAR(255),
    [notifications] NVARCHAR(255),
    [permissions] NVARCHAR(255)
);
INSERT INTO [tbl_user] ([id], [full_name], [email], [role], [created_at], [phone], [address], [notifications], [permissions]) VALUES (1, N'Super Admin', N'admin@eduplatform.com', N'Admin', N'2025-06-15T10:48:07.972397', N'', N'', N'[]', N'["manage_users", "generate_reports", "system_settings"]');
INSERT INTO [tbl_user] ([id], [full_name], [email], [role], [created_at], [phone], [address], [notifications], [permissions]) VALUES (2, N'Ali Valiyev', N'ali@student.com', N'Student', N'2025-06-15T10:48:07.972397', N'998901234567', N'Tashkent, Chilonzor', N'[{"id": 1, "message": "New assignment: ''Algebra Worksheet'' in Math due by 2025-06-22.", "recipient_id": 2, "created_at": "2025-06-15T10:48:07.991376", "is_read": false, "priority": "important"}, {"id": 4, "message": "New assignment: ''Late Homework'' in History due by 2025-06-14.", "recipient_id": 2, "created_at": "2025-06-15T10:48:08.065652", "is_read": false, "priority": "important"}, {"id": 7, "message": "New assignment: ''Late Homework'' in History due by 2025-06-14T10:48:08.212501.", "recipient_id": 2, "created_at": "2025-06-15T10:48:08.212501", "is_read": false, "priority": "important"}, {"id": 10, "message": "You received a grade of 4 for assignment ''Algebra Worksheet'' in Math.", "recipient_id": 2, "created_at": "2025-06-15T10:48:08.360269", "is_read": false, "priority": "important"}, {"id": 11, "message": "You received a grade of 2 for assignment ''Algebra Worksheet'' in Math.", "recipient_id": 2, "created_at": "2025-06-15T10:48:08.491457", "is_read": false, "priority": "important"}]', NULL);
INSERT INTO [tbl_user] ([id], [full_name], [email], [role], [created_at], [phone], [address], [notifications], [permissions]) VALUES (3, N'Dilnoza Karimova', N'dilnoza@student.com', N'Student', N'2025-06-15T10:48:07.972397', N'', N'', N'[{"id": 3, "message": "New assignment: ''Algebra Worksheet'' in Math due by 2025-06-22.", "recipient_id": 3, "created_at": "2025-06-15T10:48:07.991376", "is_read": false, "priority": "important"}, {"id": 6, "message": "New assignment: ''Late Homework'' in History due by 2025-06-14.", "recipient_id": 3, "created_at": "2025-06-15T10:48:08.065652", "is_read": false, "priority": "important"}, {"id": 9, "message": "New assignment: ''Late Homework'' in History due by 2025-06-14T10:48:08.212501.", "recipient_id": 3, "created_at": "2025-06-15T10:48:08.212501", "is_read": false, "priority": "important"}]', NULL);
INSERT INTO [tbl_user] ([id], [full_name], [email], [role], [created_at], [phone], [address], [notifications], [permissions]) VALUES (4, N'Sarvar Saidov', N'sarvar@teacher.com', N'Teacher', N'2025-06-15T10:48:07.972397', N'', N'', N'[]', NULL);
INSERT INTO [tbl_user] ([id], [full_name], [email], [role], [created_at], [phone], [address], [notifications], [permissions]) VALUES (5, N'Gulnora Aliyeva', N'gulnora@parent.com', N'Parent', N'2025-06-15T10:48:07.972397', N'', N'', N'[{"id": 2, "message": "New assignment for Ali Valiyev: ''Algebra Worksheet'' in Math.", "recipient_id": 5, "created_at": "2025-06-15T10:48:07.991376", "is_read": false, "priority": "normal"}, {"id": 5, "message": "New assignment for Ali Valiyev: ''Late Homework'' in History.", "recipient_id": 5, "created_at": "2025-06-15T10:48:08.065652", "is_read": false, "priority": "normal"}, {"id": 8, "message": "New assignment for Ali Valiyev: ''Late Homework'' in History.", "recipient_id": 5, "created_at": "2025-06-15T10:48:08.212501", "is_read": false, "priority": "normal"}, {"id": 12, "message": "Warning: Your child Ali Valiyev received a low grade (2) for ''Algebra Worksheet''.", "recipient_id": 5, "created_at": "2025-06-15T10:48:08.491457", "is_read": false, "priority": "important"}]', NULL);

GO

CREATE TABLE [tbl_assignment] (
    [id] INT PRIMARY KEY,
    [title] NVARCHAR(255),
    [description] NVARCHAR(255),
    [deadline] NVARCHAR(255),
    [subject] NVARCHAR(255),
    [teacher_id] INT,
    [class_id] NVARCHAR(255),
    [difficulty] NVARCHAR(255),
    [status] NVARCHAR(255),
    [submissions] NVARCHAR(255),
    [grades] NVARCHAR(255)
);
INSERT INTO [tbl_assignment] ([id], [title], [description], [deadline], [subject], [teacher_id], [class_id], [difficulty], [status], [submissions], [grades]) VALUES (1, N'Algebra Worksheet', N'Complete exercises 1-10', N'2025-06-22', N'Math', 4, N'9-A', N'Medium', N'Graded', N'{"2": {"content": "My completed algebra work.", "timestamp": "2025-06-15T10:48:08.132927", "is_late": false}}', N'{"2": 2}');
INSERT INTO [tbl_assignment] ([id], [title], [description], [deadline], [subject], [teacher_id], [class_id], [difficulty], [status], [submissions], [grades]) VALUES (2, N'Late Homework', N'Write an essay on World War II', N'2025-06-14', N'History', 4, N'9-A', N'Hard', N'Pending', N'{}', N'{}');
INSERT INTO [tbl_assignment] ([id], [title], [description], [deadline], [subject], [teacher_id], [class_id], [difficulty], [status], [submissions], [grades]) VALUES (3, N'Late Homework', N'This was due yesterday', N'2025-06-14', N'History', 4, N'9-A', N'Easy', N'Late Submission', N'{"3": {"content": "My very late history essay.", "timestamp": "2025-06-15T10:48:08.281549", "is_late": true}}', N'{}');

GO

CREATE TABLE [tbl_grade] (
    [id] INT PRIMARY KEY,
    [student_id] INT,
    [subject] NVARCHAR(255),
    [value] INT,
    [date] NVARCHAR(255),
    [teacher_id] INT,
    [comment] NVARCHAR(255)
);
INSERT INTO [tbl_grade] ([id], [student_id], [subject], [value], [date], [teacher_id], [comment]) VALUES (2, 2, N'Math', 4, N'2025-06-15T10:48:08.360269', 4, N'Good effort!');
INSERT INTO [tbl_grade] ([id], [student_id], [subject], [value], [date], [teacher_id], [comment]) VALUES (4, 2, N'Math', 2, N'2025-06-15T10:48:08.491457', 4, N'Needs more practice.');

GO

-- No data for tbl_schedule
