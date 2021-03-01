from accounts.models import User
from django.test import TestCase
from django.urls import reverse


class SignUpViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)

    def test_signup_form_used_and_success_url(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "username": "testuser1",
                "password1": "1X<ISRUkw+tuK",
                "password2": "1X<ISRUkw+tuK",
                "email": "test@viewstests.com",
            },
        )
        self.assertRedirects(response, "/accounts/login/")

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")

    def test_user_object_created_and_fields_are_accurate(self):
        response = self.client.post(
            reverse("signup"),
            data={
                "username": "testuser1",
                "password1": "1X<ISRUkw+tuK",
                "password2": "1X<ISRUkw+tuK",
                "email": "test@viewstests.com",
            },
        )

        # Check that the new record exists and each field has the correct data
        user = User.objects.get(username="testuser1")
        self.assertTrue(user)
        self.assertEqual(user.username, "testuser1")
        self.assertEqual(user.email, "test@viewstests.com")


class UserDetailViewTest(TestCase):
    def setUp(self):
        # Create test users
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("user-detail", args=["testuser1"]))
        self.assertRedirects(
            response, "/accounts/login/?next=/accounts/users/testuser1"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("user-detail", args=["testuser1"]))

        # Check that user is logged in
        self.assertEqual(str(response.context["user"]), "testuser1")

        # Check that response is "success"
        self.assertEqual(response.status_code, 200)

        # Check correct template was used
        self.assertTemplateUsed(response, "registration/user_detail.html")

    def test_get_object_returns_current_user(self):
        user = User.objects.get(username="testuser1")
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("user-detail", args=["testuser1"]))
        self.assertEqual(response.context["user"], user)
