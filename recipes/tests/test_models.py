from django.test import TestCase
from recipes.models import Recipe, Ingredient, Instruction


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Recipe.objects.create(
            name="Pizza", servings="8", nota_bene="It's also good cold and a day old!"
        )

    def test_name_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_servings_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("servings").verbose_name
        self.assertEqual(field_label, "servings")

    def test_nota_bene_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field("nota_bene").verbose_name
        self.assertEqual(field_label, "N.B.")

    def test_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_name(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), "Pizza")

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), "/recipes/recipe/1")


class IngredientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        recipe = Recipe.objects.create(name="Pasta", servings="4", nota_bene="")
        Ingredient.objects.create(
            recipe=recipe,
            name="Garlic",
            amount="2 to 3 cloves",
            preparation="finely minced",
        )

    def test_name_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_amount_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field("amount").verbose_name
        self.assertEqual(field_label, "amount")

    def test_amount_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field("preparation").verbose_name
        self.assertEqual(field_label, "preparation")

    def test_name_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_amount_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field("amount").max_length
        self.assertEqual(max_length, 20)

    def test_preparation_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field("preparation").max_length
        self.assertEqual(max_length, 100)

    def test_object_name_is_amount_name_comma_preparation(self):
        ingredient = Ingredient.objects.get(id=1)
        self.assertEqual(str(ingredient), "2 to 3 cloves Garlic, finely minced")


class InstructionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        recipe = Recipe.objects.create(name="Pasta", servings="4", nota_bene="")
        Instruction.objects.create(
            recipe=recipe, step_number=1, description="Bring water to boil."
        )

    def test_step_number_label(self):
        instruction = Instruction.objects.get(id=1)
        field_label = instruction._meta.get_field("step_number").verbose_name
        self.assertEqual(field_label, "Step")

    def test_description_label(self):
        instruction = Instruction.objects.get(id=1)
        field_label = instruction._meta.get_field("description").verbose_name
        self.assertEqual(field_label, "Instruction")

    def test_object_name_is_recipe_name_colon_step_number(self):
        instruction = Instruction.objects.get(id=1)
        self.assertEqual(str(instruction), "Pasta: Step 1")
