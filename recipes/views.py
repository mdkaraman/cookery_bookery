import re

from django.shortcuts import render
from recipes.models import Recipe, Ingredient, Instruction
from django.views import generic
from .forms import RecipeForm, IngredientForm, InstructionForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


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


"""********************** CUSTOM MIXINS ********************************************"""

class CustomCreateMixin:
    """ Custom mixin used by CreateViews for Recipe, Ingredient and Instruction models. """

    def dispatch(self, request, *args, **kwargs):
        path = request.path
        if 'ingredient' in path or 'instruction' in path:
            # Gets the associated recipe if this is an ingredient or instruction view 
            self.recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        else:
            # Sets the recipe to None if this is a recipe view (Recipe model has no 'recipe' field!)
            self.recipe = None
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the recipe as additional context for the template
        context['recipe'] = self.recipe
        return context

    def form_valid(self, form):
        # Set the recipe field on the form and save
        form.instance.recipe = self.recipe
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        # Send user to the appropirate 'add' page based on the type of object that was created 
        if isinstance(self.object, Recipe):
            return reverse('add-ingredient', kwargs={'pk': self.object.id})
        elif isinstance(self.object, Ingredient):
            return reverse('add-ingredient', kwargs={'pk': self.object.recipe.id})
        else:
            return reverse('add-instruction', kwargs={'pk': self.object.recipe.id})


class CustomUpdateMixin:
    """ Custom mixin used by UpdateViews for Recipe, Ingredient and Instruction models. """
    
    def dispatch(self, request, *args, **kwargs):
        # Get previous page url to use in success url
        self.next = request.GET.get('next', '/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract recipe id from query parameter 
        recipe_id = re.findall(r'[0-9]+', self.next)[0]
        context['recipe'] = Recipe.objects.get(id=recipe_id)
        context['pk'] = self.object.id
        # Used by template to render update-specific messages and formatting 
        context['update'] = True
        # Used by ingredient template for maintaining visual consistency with the next page rendered
        context['instruction_next'] = 'instruction' in self.next
        return context
    
    def get_success_url(self):
        # Send user back to the previous page
        return self.next

class CustomDeleteMixin:
    """ Custom mixin used by DeleteViews for Recipe, Ingredient and Instruction models. """
    
    def dispatch(self, request, *args, **kwargs):
        # Get previous page url to use in success url
        self.next = request.POST.get('next', '/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe
        context['pk'] = self.object.id
        return context

    def get_success_url(self):
        # Send user back to the previous page
        return self.next

"""*********************************************************************************"""


class RecipeCreate(LoginRequiredMixin, CustomCreateMixin, CreateView):
    model = Recipe
    fields = ['name', 'servings', 'nota_bene']

class RecipeUpdate(LoginRequiredMixin, CustomUpdateMixin, UpdateView):
    model = Recipe
    fields = ['name', 'servings', 'nota_bene']

class IngredientCreate(LoginRequiredMixin, CustomCreateMixin, CreateView):
    model = Ingredient
    fields = ['name', 'amount', 'preparation']
    
class IngredientUpdate(LoginRequiredMixin, CustomUpdateMixin, UpdateView):
    model = Ingredient
    fields = ['name', 'amount', 'preparation']

class IngredientDelete(LoginRequiredMixin, CustomDeleteMixin, DeleteView):
    model = Ingredient
 
class InstructionCreate(LoginRequiredMixin, CustomCreateMixin, CreateView):
    model = Instruction
    fields = ['step_number', 'description']
    
class InstructionUpdate(LoginRequiredMixin, CustomUpdateMixin, UpdateView):
    model = Instruction
    fields = ['step_number', 'description']
 
class InstructionDelete(LoginRequiredMixin, CustomDeleteMixin, DeleteView):
    model = Instruction
   