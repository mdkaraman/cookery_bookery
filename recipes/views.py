from django.shortcuts import render
from recipes.models import Recipe, Ingredient, Instruction
from django.views import generic
from .forms import RecipeForm, IngredientForm, InstructionForm
from django.http import HttpResponseRedirect
from django.urls import reverse


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

def user_submit_recipe(request):
    """View function for user recipe submission page."""

    form = RecipeForm(request.POST)

    if request.method == 'POST':
        

        if form.is_valid():
            recipe = Recipe.objects.create(
                name=form.cleaned_data['name'],
                servings=form.cleaned_data['servings'],
                nota_bene=form.cleaned_data['nota_bene']
            )
    
            return HttpResponseRedirect(reverse('recipe-detail', args=[recipe.id]))
    else:
        pass

    context = {
        'form': form,
    }

    return render(request, 'recipes/submit_recipe.html', context)