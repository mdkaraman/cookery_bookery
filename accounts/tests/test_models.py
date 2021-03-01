from accounts.models import User
from django.test import TestCase


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test user
        User.objects.create_user(
            username="Jake",
            password="oedipusrex",
            email="forgetit@chinatown.com",
        )

    def test_favorite_recipes_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field("favorite_recipes").verbose_name
        self.assertEqual(field_label, "favorite recipes")

    def test_object_name_is_username(self):
        user = User.objects.get(id=1)
        self.assertEqual(str(user), "Jake")
