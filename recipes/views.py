import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from recipes.models import Ingredient, Instruction, Recipe

from .forms import IngredientForm, InstructionForm, RecipeForm


class IndexView(generic.TemplateView):
    """ View class for home page of site. """

    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get 9 newest recipes
        newest_recipes = list(Recipe.objects.order_by("-pk")[:9])
        
        for recipe in newest_recipes:
            # A description is too long for the display box if it is over 100 chars
            if len(recipe.description) > 100:
                # Truncate the long description and add ellipsis
                recipe.description = recipe.description[:99] + "..."

        # Prepare the context variable for the new recipes list
        context["newest_recipes"] = []
        for i in range(len(newest_recipes)):
            if i % 3 == 0:
                # Add the recipes in lists of 3 for template rendering purposes
                context["newest_recipes"].append(newest_recipes[i:i+3])
        
        return context


class RecipeListView(generic.ListView):
    """ Generic list view for displaying all recipes. """

    model = Recipe
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get user's favorite recipes
            context["favorites"] = self.request.user.favorite_recipes.all()
        return context


class RecipeDetailView(generic.DetailView):
    """ Generic detail view for displaying individual recipes. """

    model = Recipe

    def dispatch(self, request, *args, **kwargs):
        recipe = self.get_object()
        # Check if an add/remove action is being performed
        action = request.GET.get("action")
        if action == "favorite":
            # Add the recipe to the user's favorites
            self.request.user.favorite_recipes.add(recipe)
        elif action == "remove":
            # Remove the recipe from the user's favorites
            request.user.favorite_recipes.remove(recipe)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get user's favorite recipes
            context["favorites"] = self.request.user.favorite_recipes.all()
        return context


class MyRecipesListView(LoginRequiredMixin, generic.ListView):
    """ Generic list view for a user's submitted recipes. """

    model = Recipe
    template_name = "recipes/my_recipes_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Recipe.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Get user's favorite recipes
            context["favorites"] = self.request.user.favorite_recipes.all()
        return context


class MyFavoritesListView(LoginRequiredMixin, generic.ListView):
    """ Generic list view for viewing a user's favorite recipes. """

    model = Recipe
    template_name = "recipes/my_favorites_list.html"
    paginate_by = 10

    def dispatch(self, request, *args, **kwargs):
        # Check if a recipe needs to be removed from favorites
        remove_action = request.GET.get("action")
        if remove_action:
            # Get the recipe and remove it
            recipe_id = int(re.findall(r"[0-9]+", remove_action)[0])
            recipe = Recipe.objects.get(id=recipe_id)
            request.user.favorite_recipes.remove(recipe)
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.request.user.favorite_recipes.all()


""" ********************* CUSTOM MIXINS *************************** """


class CustomCreateMixin:
    """ Custom mixin used by Recipe, Ingredient and Instruction create views. """

    def dispatch(self, request, *args, **kwargs):
        path = request.path
        # Assume this is a recipe view
        self.is_recipe = True
        if "ingredient" in path or "instruction" in path:
            # This is an ingredient or instruction view, so get the recipe
            self.recipe = get_object_or_404(Recipe, pk=kwargs["pk"])
            self.is_recipe = False
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if this is an ingredient or instruction view
        if not self.is_recipe:
            # Add the recipe as additional context for the template
            context["recipe"] = self.recipe
        return context

    def form_valid(self, form):
        if self.is_recipe:
            # Set the owner field on the recipe form
            form.instance.author = self.request.user
            # Guarantee the name starts in uppercase (for proper ordering)
            uppercase_name = form.instance.name[0].upper() + form.instance.name[1:]
            form.instance.name = uppercase_name
        else:
            # Set the recipe field on the ingredient/instruction form
            form.instance.recipe = self.recipe

        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        # Send user to add ingredient page if a recipe or ingredient was just created
        if isinstance(self.object, Recipe):
            return reverse("add-ingredient", kwargs={"pk": self.object.id})
        elif isinstance(self.object, Ingredient):
            return reverse("add-ingredient", kwargs={"pk": self.object.recipe.id})
        else:
            # Send user to add instruction page if an instruction was just created
            return reverse("add-instruction", kwargs={"pk": self.object.recipe.id})


class CustomUpdateOrDeleteMixin:
    """ Base class inherited by CustomUpdate and CustomDelete mixins. """

    def dispatch(self, request, *args, **kwargs):
        # Get previous page url to use in success url
        self.next = request.GET.get("next", "/")
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        # Send user back to the previous page
        return self.next


class CustomUpdateMixin(CustomUpdateOrDeleteMixin):
    """ Custom mixin used by Recipe, Ingredient and Instruction update views. """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Extract recipe id from query parameter
        recipe_id = re.findall(r"[0-9]+", self.next)[0]
        context["recipe"] = Recipe.objects.get(id=recipe_id)
        context["pk"] = self.object.id
        # Used by template to render update-specific messages and formatting
        context["update"] = True
        # Used by ingredient template for maintaining visual consistency with next page
        context["instruction_next"] = "instruction" in self.next
        return context


class CustomDeleteMixin(CustomUpdateOrDeleteMixin):
    """ Custom mixin used by Recipe, Ingredient and Instruction delete views. """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipe"] = self.object.recipe
        context["pk"] = self.object.id
        return context


""" *************************************************************** """


class RecipeCreate(LoginRequiredMixin, CustomCreateMixin, CreateView):
    model = Recipe
    form_class = RecipeForm


class RecipeUpdate(LoginRequiredMixin, CustomUpdateMixin, UpdateView):
    model = Recipe
    form_class = RecipeForm


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    success_url = reverse_lazy("my-recipes")


class IngredientCreate(LoginRequiredMixin, CustomCreateMixin, CreateView):
    model = Ingredient
    form_class = IngredientForm


class IngredientUpdate(LoginRequiredMixin, CustomUpdateMixin, UpdateView):
    model = Ingredient
    form_class = IngredientForm


class IngredientDelete(LoginRequiredMixin, CustomDeleteMixin, DeleteView):
    model = Ingredient


class InstructionCreate(LoginRequiredMixin, CustomCreateMixin, CreateView):
    model = Instruction
    form_class = InstructionForm


class InstructionUpdate(LoginRequiredMixin, CustomUpdateMixin, UpdateView):
    model = Instruction
    form_class = InstructionForm


class InstructionDelete(LoginRequiredMixin, CustomDeleteMixin, DeleteView):
    model = Instruction
