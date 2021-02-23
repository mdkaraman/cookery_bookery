from django.test import TestCase
from recipes.models import Recipe, Ingredient, Instruction


class RecipeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Recipe.object.create(name='Pizza', servings='8', nota_bene="It's also good cold and a day old!")

    def test_name_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'name')
    
    def test_servings_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('servings').verbose_name
        self.assertEqual(field_label, 'servings')

    def test_nota_bene_label(self):
        recipe = Recipe.objects.get(id=1)
        field_label = recipe._meta.get_field('nota_bene').verbose_name
        self.assertEqual(field_label, 'N.B.')

    def test_name_max_length(self):
        recipe = Recipe.objects.get(id=1)
        max_length = recipe._meta.get_field('name').max_length
        assertEqual(max_length, 200)
    
    def test_str_is_name(self)
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(str(recipe), 'Pizza')

    def test_get_absolute_url(self):
        recipe = Recipe.objects.get(id=1)
        self.assertEqual(recipe.get_absolute_url(), '/recipes/recipe/1')
