from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from recipes.models import Recipe, Ingredient, Instruction

from recipes.views import CustomCreateMixin
from recipes.views import CustomUpdateOrDeleteMixin
from recipes.views import CustomUpdateMixin, CustomDeleteMixin

from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import HttpResponse


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test recipes
        number_of_recipes = 15
        for recipe_id in range(number_of_recipes):
            Recipe.objects.create(name=f"Recipe {recipe_id}", servings=2, nota_bene="")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/recipes/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")

    def test_displays_ten_most_recent_recipes(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("newest_recipes" in response.context)

        # Check that 10 recipes are in the template's context
        self.assertTrue(len(response.context["newest_recipes"]) == 10)

        # Check that recipes are listed newest to oldest
        newest_recipes = response.context["newest_recipes"]
        recipe_id = 15
        for recipe in newest_recipes:
            self.assertTrue(recipe.id == recipe_id)
            recipe_id -= 1


class RecipeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create test recipes
        number_of_recipes = 15
        for recipe_id in range(number_of_recipes):
            Recipe.objects.create(name=f"Recipe {recipe_id}", servings=2, nota_bene="")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/recipes/all-recipes/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("all-recipes"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("all-recipes"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_list.html")

    def test_pagination_is_ten(self):
        response = self.client.get(reverse("all-recipes"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["recipe_list"]) == 10)

    def test_lists_all_recipes(self):
        # Get second page and confirm it has exactly 5 remaining items
        response = self.client.get(reverse("all-recipes") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["recipe_list"]) == 5)


class RecipeDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        recipe = Recipe.objects.create(name="Pizza", servings=8)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/recipes/recipe/1")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("recipe-detail", args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("recipe-detail", args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")


class MyRecipesListViewTest(TestCase):
    def setUp(self):
        # Create test users
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user2 = User.objects.create_user(
            username="testuser2", password="2HJ1vRV0Z&3iD"
        )
        test_user1.save()
        test_user2.save()

        # Create recipes for test_user1
        number_of_recipes = 15
        for recipe_id in range(number_of_recipes):
            Recipe.objects.create(
                name=f"Recipe {recipe_id}", servings=2, nota_bene="", author=test_user1
            )
        # Create recipes for test_user2
        number_of_recipes = 15
        for recipe_id in range(number_of_recipes, 2 * number_of_recipes):
            Recipe.objects.create(
                name=f"Recipe {recipe_id}", servings=2, nota_bene="", author=test_user2
            )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("my-recipes"))
        self.assertRedirects(response, "/accounts/login/?next=/recipes/my-recipes/")

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("my-recipes"))

        # Check that user is logged in
        self.assertEqual(str(response.context["user"]), "testuser1")

        # Check that response is "success"
        self.assertEqual(response.status_code, 200)

        # Check correct template was used
        self.assertTemplateUsed(response, "recipes/my_recipes_list.html")

    def test_pagination_is_ten(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("my-recipes"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertTrue(len(response.context["recipe_list"]) == 10)

    def test_lists_only_user_recipes(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("my-recipes"))
        self.assertEqual(response.status_code, 200)

        # Check that all recipes in the list belong to logged in user
        self.assertTrue("recipe_list" in response.context)
        for recipe in response.context["recipe_list"]:
            self.assertEqual(response.context["user"], recipe.author)

        # Log in a new user and check again
        login = self.client.login(username="testuser2", password="2HJ1vRV0Z&3iD")
        response = self.client.get(reverse("my-recipes"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("recipe_list" in response.context)
        for recipe in response.context["recipe_list"]:
            self.assertEqual(response.context["user"], recipe.author)


class RecipeCreateViewTest(TestCase):
    def setUp(self):
        # Create test user
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("create-recipe"))
        self.assertRedirects(
            response, "/accounts/login/?next=/recipes/submit-recipe/create"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("create-recipe"))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_form.html")


class CustomCreateMixinTest(TestCase):

    factory = RequestFactory()

    @classmethod
    def setUp(self):
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

        recipe = Recipe.objects.create(name="Pizza", servings=8)

    def test_custom_create_mixin(self):

        # Create a dummy view to hold the mixin
        class AView(CustomCreateMixin, CreateView):
            # Return an empty response
            def get(self, request, *args, **kwargs):
                return HttpResponse()

        view = AView.as_view()

        # self.factory.path = '/recipes/submit-recipe/1/add-ingredient'
        user = User.objects.filter(username="test_user1")
        request = self.factory.get("/recipes/submit-recipe/create")
        request.user = user
        response = view(request)

        self.assertEqual(response.status_code, 200)


"""
    class DummyRecipeCreateView(CustomCreateMixin, CreateView):
        model = Recipe
        #fields = ['name', 'servings', 'nota_bene']



    def setUp(cls):
        # Create test users
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user2 = User.objects.create_user(username='testuser2', password='2HJ1vRV0Z&3iD')

        test_user1.save()
        test_user2.save()

        # Create recipe
        recipe = Recipe.objects.create(name='Pasta', servings='4', nota_bene='')
"""
