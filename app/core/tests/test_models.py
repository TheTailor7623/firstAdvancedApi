"""
Tests for models
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    """Tests models"""

    def test_create_user_with_email_successful(self):
        """Tests creating a user with a valid email is successful"""
        # Arrange
        input_case = {
            "email":"test@example.com",
            "password":"testpass123",
        }

        expected = {
            "email":"test@example.com",
        }

        systemUnderTest = get_user_model().objects.create_user

        # Act
        actual = systemUnderTest(*input_case)

        # Assert
        self.assertEqual(actual.email, expected["email"])
        self.assertTrue(actual.check_password(input_case["password"]))