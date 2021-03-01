from accounts.forms import SignUpForm
from accounts.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


class SignUpFormTest(TestCase):
    def test_username_max_length(self):
        # Build a username string longer than 150 characters
        long_username = ["a"] * 151
        form = SignUpForm(
            data={
                "username": long_username,
                "password": "test12345",
                "email": "test@formstests.com",
            }
        )
        self.assertFalse(form.is_valid())

    def test_email_max_length(self):
        # Build an email string longer than 150 characters
        long_email = ["a"] * 200 + ["@testemail.com"]
        form = SignUpForm(
            data={"username": "test_user", "password": "test12345", "email": long_email}
        )
        self.assertFalse(form.is_valid())

    def test_email_must_not_already_exist(self):
        # Create a test user
        test_user1 = User.objects.create(
            username="test_user1", password="test12345", email="test@formstests.com"
        )
        # Create a signup form with the same email
        form = SignUpForm(
            data={
                "username": "test_user2",
                "password": "test67890",
                "email": "test@formstests.com",
            }
        )
        self.assertFalse(form.is_valid())
