from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from recipes.models import Recipe, Ingredient, Instruction

from recipes.views import CustomCreateMixin
from recipes.views import CustomUpdateOrDeleteMixin
from recipes.views import CustomUpdateMixin, CustomDeleteMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView


class IndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        number_of_recipes = 15

        for recipe_id in range(number_of_recipes):
            Recipe.objects.create(
                name=f'Recipe {recipe_id}',
                servings=2,
                nota_bene=''
            )
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
    
    def test_displays_ten_most_recent_recipes(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('newest_recipes' in response.context)
        self.assertTrue(len(response.context['newest_recipes']) == 10)

        newest_recipes = response.context['newest_recipes']
        recipe_id = 15
        for recipe in newest_recipes:
            self.assertTrue(recipe.id == recipe_id)
            recipe_id -= 1

class RecipeListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        
        number_of_recipes = 15

        for recipe_id in range(number_of_recipes):
            Recipe.objects.create(
                name=f'Recipe {recipe_id}',
                servings=2,
                nota_bene=''
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/all-recipes/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('all-recipes'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('all-recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_list.html')

    def test_pagination_is_ten(self):
        response = self.client.get(reverse('all-recipes'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['recipe_list']) == 10)

    def test_lists_all_recipes(self):
        response = self.client.get(reverse('all-recipes')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['recipe_list']) == 5)

class RecipeDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        recipe = Recipe.objects.create(name='Pizza', servings=8)

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/recipes/recipe/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('recipe-detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('recipe-detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_detail.html')


class RecipeCreateViewTest(TestCase):
    
    def setUp(self):
        test_user1 = User.objects.create_user(username='testuser1', password='1X<ISRUkw+tuK')
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('create-recipe'))
        self.assertRedirects(response, '/accounts/login/?next=/recipes/submit-recipe/create')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='1X<ISRUkw+tuK')
        response = self.client.get(reverse('create-recipe'))
        self.assertEqual(str(response.context['user']), 'testuser1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/recipe_form.html')
'''
class CustomCreateMixinTest(TestCase):
    
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
'''