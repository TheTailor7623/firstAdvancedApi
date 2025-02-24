"""
This file tests the task manager (any related code to the task manager)
"""

from django.test import TestCase
from core import models
from django.contrib.auth import get_user_model

from datetime import datetime

class ValidScenariosTaskManagerTests(TestCase):
    """This class is built to test the task manager"""

    def test_creating_task_with_all_task_details(self):
        """Test creating a task"""
        # Arrange
        user = get_user_model().objects.create_user(
            email="test100@example.com",
            firstname="TestFirstname",
            surname="TestLastname",
            date_of_birth="2003-10-18",
            city="london",
            password="Testpass123",
        )

        input_data = {
            "task_title":"Test task title",
            "task_description":"Test task description",
            "task_importance_level":"high",
            "task_importance_magnitude":10,
            "task_urgency_level":"low",
            "task_urgency_magnitude":15,
            "task_deadline": datetime(2025, 4, 10, 12, 0),
            "task_start": datetime(2025, 1, 10, 9, 0),
            "task_end": datetime(2025, 4, 10, 17, 0),
            "task_status":"to-do",
        }
        systemUnderTest = models.TasksModel

        # Act
        actual = systemUnderTest.objects.create(
            user=user,
            **input_data,
        )

        # Assert
        self.assertEqual(actual.task_title, input_data["task_title"])
        # print(f"First assert \n Actual={actual.task_title} - Input={input_data["task_title"]}")
        self.assertEqual(actual.task_description, input_data["task_description"])
        # print(f"First assert \n Actual={actual.task_description} - Input={input_data["task_description"]}")
        self.assertEqual(actual.task_importance_level, input_data["task_importance_level"])
        # print(f"First assert \n Actual={actual.task_importance_level} - Input={input_data["task_importance_level"]}")
        self.assertEqual(actual.task_importance_magnitude, input_data["task_importance_magnitude"])
        # print(f"First assert \n Actual={actual.task_importance_magnitude} - Input={input_data["task_importance_magnitude"]}")
        self.assertEqual(actual.task_urgency_level, input_data["task_urgency_level"])
        # print(f"First assert \n Actual={actual.task_urgency_level} - Input={input_data["task_urgency_level"]}")
        self.assertEqual(actual.task_urgency_magnitude, input_data["task_urgency_magnitude"])
        # print(f"First assert \n Actual={actual.task_urgency_magnitude} - Input={input_data["task_urgency_magnitude"]}")
        self.assertEqual(actual.task_deadline, input_data["task_deadline"])
        # print(f"First assert \n Actual={actual.task_deadline} - Input={input_data["task_deadline"]}")
        self.assertEqual(actual.task_start, input_data["task_start"])
        # print(f"First assert \n Actual={actual.task_start} - Input={input_data["task_start"]}")
        self.assertEqual(actual.task_end, input_data["task_end"])
        # print(f"First assert \n Actual={actual.task_end} - Input={input_data["task_end"]}")
        self.assertEqual(actual.task_status, input_data["task_status"])
        # print(f"First assert \n Actual={actual.task_status} - Input={input_data["task_status"]}")
        self.assertEqual(actual.user, user)
        # print(f"First assert \n Actual={actual.user} - Input={user}")