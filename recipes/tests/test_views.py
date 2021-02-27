from accounts.models import User

# from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from django.urls import reverse
from recipes.models import Ingredient, Instruction, Recipe


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

    def test_recipe_object_created_and_fields_are_accurate(self):
        user = User.objects.get(pk=1)
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.post(
            reverse("create-recipe"),
            {
                "name": "Pizza",
                "servings": "8",
                "author": "test_user1",
            },
        )
        # Check that the new record exists and each field has the correct data
        recipe = Recipe.objects.get(pk=1)
        self.assertTrue(recipe)
        self.assertEqual(recipe.name, "Pizza")
        self.assertEqual(recipe.servings, 8)
        self.assertEqual(recipe.nota_bene, "")
        self.assertEqual(recipe.author, user)


class IngredientCreateViewTest(TestCase):
    def setUp(self):
        # Create test user and recipe
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()
        recipe = Recipe.objects.create(name="Pizza", servings=8, author=test_user1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("add-ingredient", kwargs={"pk": 1}))
        self.assertRedirects(
            response, "/accounts/login/?next=/recipes/submit-recipe/1/add-ingredient"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("add-ingredient", kwargs={"pk": 1}))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/ingredient_form.html")

    def test_ingredient_object_created_and_fields_are_accurate(self):
        user = User.objects.get(pk=1)
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        recipe = Recipe.objects.get(pk=1)
        response = self.client.post(
            reverse("add-ingredient", kwargs={"pk": 1}),
            {
                "recipe": recipe,
                "name": "Mozzarella",
                "amount": "12 oz.",
                "preparation": "shredded",
            },
        )
        # Check that the new record exists and each field has the correct data
        ingredient = Ingredient.objects.get(pk=1)
        self.assertTrue(ingredient)
        self.assertEqual(ingredient.recipe, recipe)
        self.assertEqual(ingredient.name, "Mozzarella")
        self.assertEqual(ingredient.amount, "12 oz.")
        self.assertEqual(ingredient.preparation, "shredded")


class InstructionCreateViewTest(TestCase):
    def setUp(self):
        # Create test user and recipe
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()
        recipe = Recipe.objects.create(name="Pizza", servings=8, author=test_user1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("add-instruction", kwargs={"pk": 1}))
        self.assertRedirects(
            response, "/accounts/login/?next=/recipes/submit-recipe/1/add-instruction"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("add-instruction", kwargs={"pk": 1}))
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/instruction_form.html")

    def test_ingredient_object_created_and_fields_are_accurate(self):
        user = User.objects.get(pk=1)
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        recipe = Recipe.objects.get(pk=1)
        response = self.client.post(
            reverse("add-instruction", kwargs={"pk": 1}),
            {
                "recipe": recipe,
                "step_number": "1",
                "description": "Knead the dough.",
            },
        )
        # Check that the new record exists and each field has the correct data
        instruction = Instruction.objects.get(pk=1)
        self.assertTrue(instruction)
        self.assertEqual(instruction.recipe, recipe)
        self.assertEqual(instruction.step_number, 1)
        self.assertEqual(instruction.description, "Knead the dough.")


class RecipeUpdateViewTest(TestCase):
    def setUp(self):
        # Create test user, recipe and ingredient
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

        recipe = Recipe.objects.create(name="Pizza", servings=8, author=test_user1)
        ingredient = Ingredient.objects.create(
            recipe=recipe, name="Dough", amount="12 oz."
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("update-recipe", kwargs={"pk": 1}))
        self.assertRedirects(
            response, "/accounts/login/?next=/recipes/submit-recipe/1/update_recipe"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        # Use hard-coded url since the view relies on the 'next' query parameter
        response = self.client.get(
            "/recipes/submit-recipe/1/update_recipe?next=/recipes/submit-recipe/1/add-ingredient"
        )
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_form.html")

    def test_recipe_fields_update_accurately(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        user = User.objects.get(pk=1)
        # Use hard-coded url since the view relies on the 'next' query parameter
        response = self.client.post(
            "/recipes/submit-recipe/1/update_recipe?next=/recipes/submit-recipe/1/add-ingredient",
            {
                "name": "Pepperoni Pizza",
                "servings": "10",
                "nota_bene": "Spicy!",
                "author": "test_user1",
            },
        )
        recipe = Recipe.objects.get(pk=1)
        self.assertEqual(recipe.name, "Pepperoni Pizza")
        self.assertEqual(recipe.servings, 10)
        self.assertEqual(recipe.nota_bene, "Spicy!")
        self.assertEqual(recipe.author, user)


class IngredientUpdateViewTest(TestCase):
    def setUp(self):
        # Create test user, recipe and ingredient
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

        recipe = Recipe.objects.create(name="Pizza", servings=8, author=test_user1)
        ingredient = Ingredient.objects.create(
            recipe=recipe, name="Dough", amount="12 oz."
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("update-ingredient", kwargs={"pk": 1}))
        self.assertRedirects(
            response, "/accounts/login/?next=/recipes/submit-recipe/1/update_ingredient"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        # Use hard-coded url since the view relies on the 'next' query parameter
        response = self.client.get(
            "/recipes/submit-recipe/1/update_ingredient?next=/recipes/submit-recipe/1/add-ingredient"
        )
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/ingredient_form.html")

    def test_recipe_fields_update_accurately(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        user = User.objects.get(pk=1)
        # Use hard-coded url since the view relies on the 'next' query parameter
        response = self.client.post(
            "/recipes/submit-recipe/1/update_ingredient?next=/recipes/submit-recipe/1/add-ingredient",
            {
                "name": "Pizza Dough",
                "amount": "14 oz.",
                "preparation": "room temperature",
            },
        )
        recipe = Ingredient.objects.get(pk=1)
        self.assertEqual(recipe.name, "Pizza Dough")
        self.assertEqual(recipe.amount, "14 oz.")
        self.assertEqual(recipe.preparation, "room temperature")


class InstructionUpdateViewTest(TestCase):
    def setUp(self):
        # Create test user, recipe and instruction
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

        recipe = Recipe.objects.create(name="Pizza", servings=8, author=test_user1)
        instruction = Instruction.objects.create(
            recipe=recipe, step_number=1, description="Preheat the oven."
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("update-instruction", kwargs={"pk": 1}))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/recipes/submit-recipe/1/update_instruction",
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        # Use hard-coded url since the view relies on the 'next' query parameter
        response = self.client.get(
            "/recipes/submit-recipe/1/update_instruction?next=/recipes/submit-recipe/1/add-instruction"
        )
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/instruction_form.html")

    def test_recipe_fields_update_accurately(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        user = User.objects.get(pk=1)
        # Use hard-coded url since the view relies on the 'next' query parameter
        response = self.client.post(
            "/recipes/submit-recipe/1/update_instruction?next=/recipes/submit-recipe/1/add-instruction",
            {
                "step_number": "1",
                "description": "Preheat the oven to 500 degrees Fahrenheit.",
            },
        )
        recipe = Instruction.objects.get(pk=1)
        self.assertEqual(recipe.step_number, 1)
        self.assertEqual(
            recipe.description, "Preheat the oven to 500 degrees Fahrenheit."
        )


def RecipeDeleteViewTest(TestCase):
    def setUp(self):
        # Create test user and recipe
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

        recipe = Recipe.objects.create(name="Pizza", servings=8, author=test_user1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("delete-recipe", kwargs={"pk": 1}))
        self.assertRedirects(
            response, "/accounts/login/?next=/recipes/recipe/1/delete-recipe"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("delete-recipe"), kwargs={"pk": 1})
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/recipe_confirm_delete.html")

    def test_deletes_record_successfully(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        user = User.objects.get(pk=1)
        response = self.client.post(reverse("delete-recipe", kwargs={"pk": 1}))
        self.assertRaises(ObjectDoesNotExist, Recipe.objects.get, pk=1)


def IngredientDeleteViewTest(TestCase):
    def setUp(self):
        # Create test user, recipe and ingredient
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

        recipe = Recipe.objects.create(name="Pizza", servings=8, author=test_user1)
        ingredient = Ingredient.objects.create(
            recipe=recipe, name="Dough", amount="12 oz."
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("delete-ingredient", kwargs={"pk": 1}))
        self.assertRedirects(
            response, "/accounts/login/?next=/recipes/submit_recipe/1/delete_ingredient"
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("delete-ingredient"), kwargs={"pk": 1})
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/ingredient_confirm_delete.html")

    def test_deletes_record_successfully(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        user = User.objects.get(pk=1)
        response = self.client.post(reverse("delete-ingredient", kwargs={"pk": 1}))
        self.assertRaises(ObjectDoesNotExist, Recipe.objects.get, pk=1)


def InstructionDeleteViewTest(TestCase):
    def setUp(self):
        # Create test user, recipe and instruction
        test_user1 = User.objects.create_user(
            username="testuser1", password="1X<ISRUkw+tuK"
        )
        test_user1.save()

        recipe = Recipe.objects.create(name="Pizza", servings=8, author=test_user1)
        instruction = Instruction.objects.create(
            recipe=recipe, step_number=1, description="Preheat the oven."
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("delete-instruction", kwargs={"pk": 1}))
        self.assertRedirects(
            response,
            "/accounts/login/?next=/recipes/submit_recipe/1/delete_instruction",
        )

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        response = self.client.get(reverse("delete-instruction"), kwargs={"pk": 1})
        self.assertEqual(str(response.context["user"]), "testuser1")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/instruction_confirm_delete.html")

    def test_deletes_record_successfully(self):
        login = self.client.login(username="testuser1", password="1X<ISRUkw+tuK")
        user = User.objects.get(pk=1)
        response = self.client.post(reverse("delete-instruction", kwargs={"pk": 1}))
        self.assertRaises(ObjectDoesNotExist, Recipe.objects.get, pk=1)
