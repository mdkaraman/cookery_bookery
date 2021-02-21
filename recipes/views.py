from django.shortcuts import render
from recipes.models import Recipe, Ingredient, Instruction
from django.views import generic
from .forms import RecipeForm, IngredientForm, InstructionForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


def index(request):
    """View function for home page of site."""

    # Fetch the number of recipe records
    num_recipes = Recipe.objects.count()
    newest_recipes = Recipe.objects.order_by('-pk')[:10]

    context ={
        'num_recipes': num_recipes,
        'newest_recipes': newest_recipes
    }

    return render(request, 'index.html', context=context)

class RecipeListView(generic.ListView):
    model = Recipe
    paginate_by = 10

class RecipeDetailView(generic.DetailView):
    model = Recipe

@login_required
def user_submit_recipe(request):
    """View function for user recipe submission page."""

    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST)

        if recipe_form.is_valid():
            recipe = Recipe.objects.create(
                name=recipe_form.cleaned_data['name'],
                servings=recipe_form.cleaned_data['servings'],
                nota_bene=recipe_form.cleaned_data['nota_bene']
            )
            recipe.save()
            recipe_id = str(recipe.id)
            return HttpResponseRedirect(reverse('add-ingredient', args=[recipe_id]))
    else:
        recipe_form = RecipeForm()
     
    context = {
        'recipe_form': recipe_form,
    }

    return render(request, 'recipes/submit_recipe.html', context)

@login_required
def user_add_ingredient(request, pk):
    
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        ingredient_form = IngredientForm(request.POST)

        if ingredient_form.is_valid():
            ingredient = Ingredient.objects.create(
                recipe=recipe,
                name=ingredient_form.cleaned_data['name'],
                amount=ingredient_form.cleaned_data['amount'],
                preparation=ingredient_form.cleaned_data['preparation']
            )
            

            return HttpResponseRedirect(reverse('add-ingredient', args=[recipe.id]))
    else:
        ingredient_form = IngredientForm()
     
    context = {
        'ingredient_form': ingredient_form,
        'recipe': recipe,
    }

    return render(request, 'recipes/add_ingredient.html', context)

@login_required
def user_add_instruction(request, pk):
    
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        instruction_form = InstructionForm(request.POST)

        if instruction_form.is_valid():
            instruction = Instruction.objects.create(
                recipe=recipe,
                step_number=instruction_form.cleaned_data['step_number'],
                description=instruction_form.cleaned_data['description'],
            )
            
            return HttpResponseRedirect(reverse('add-instruction', args=[recipe.id]))
    else:
        instruction_form = InstructionForm()
     
    context = {
        'instruction_form': instruction_form,
        'recipe': recipe,
    }

    return render(request, 'recipes/add_instruction.html', context)

