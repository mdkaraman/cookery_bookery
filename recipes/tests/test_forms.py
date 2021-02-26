from django.test import SimpleTestCase
from recipes.forms import IngredientForm, InstructionForm, RecipeForm


class RecipeFormTest(SimpleTestCase):
    def test_recipe_form_name_field_help_text(self):
        form = RecipeForm()
        self.assertEqual(form.fields["name"].help_text, "Enter a name for this recipe")

    def test_recipe_form_servings_field_help_text(self):
        form = RecipeForm()
        self.assertEqual(
            form.fields["servings"].help_text,
            "Enter the number of servings this recipe makes",
        )

    def test_recipe_form_servings_field_help_text(self):
        form = RecipeForm()
        self.assertEqual(
            form.fields["nota_bene"].help_text,
            "Add any useful notes, hints or advice for this recipe",
        )

    def test_recipe_form_servings_must_be_one_or_more(self):
        form = RecipeForm(data={"name": "Pasta", "servings": -1})
        self.assertFalse(form.is_valid())
        form = RecipeForm(data={"name": "Pasta", "servings": 0})
        self.assertFalse(form.is_valid())
        form = RecipeForm(data={"name": "Pasta", "servings": 1})
        self.assertTrue(form.is_valid())


class IngredientFormTest(SimpleTestCase):
    def test_ingredient_form_name_field_help_text(self):
        form = IngredientForm()
        self.assertEqual(
            form.fields["name"].help_text,
            "Enter the name of an ingredient (e.g. garlic)",
        )

    def test_ingredient_form_amount_field_help_text(self):
        form = IngredientForm()
        self.assertEqual(
            form.fields["amount"].help_text, "Enter the amount to use (e.g. 1/4 tsp.)"
        )

    def test_ingredient_form_preparation_field_help_text(self):
        form = IngredientForm()
        self.assertEqual(
            form.fields["preparation"].help_text,
            'Describe this ingredient"s preparation (e.g. finely minced) or leave blank',
        )


class InstructionFormTest(SimpleTestCase):
    def test_instruction_form_step_number_field_help_text(self):
        form = InstructionForm()
        self.assertEqual(
            form.fields["step_number"].help_text,
            "Enter the step number for this instruction (e.g. step 1)",
        )

    def test_instruction_form_description_field_help_text(self):
        form = InstructionForm()
        self.assertEqual(
            form.fields["description"].help_text, "Describe this step's instructions"
        )

    def test_instruction_form_step_number_must_be_one_or_more(self):
        form = InstructionForm(
            data={"step_number": -1, "description": "Test Instruction"}
        )
        self.assertFalse(form.is_valid())
        form = InstructionForm(
            data={"step_number": 0, "description": "Test Instruction"}
        )
        self.assertFalse(form.is_valid())
        form = InstructionForm(
            data={"step_number": 1, "description": "Test Instruction"}
        )
        self.assertTrue(form.is_valid())
