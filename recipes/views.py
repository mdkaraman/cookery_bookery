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

class RecipeCreate(LoginRequiredMixin, CreateView):
    model = Recipe
    fields = ['name', 'servings', 'nota_bene']
    
    def get_success_url(self):
        return reverse('add-ingredient', kwargs={'pk': self.object.id})

class RecipeUpdate(LoginRequiredMixin, UpdateView):
    model = Recipe
    fields = ['name', 'servings', 'nota_bene']

    def dispatch(self, request, *args, **kwargs):
        self.next = request.POST.get('next', '/')
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return self.next

class IngredientCreate(LoginRequiredMixin, CreateView):
    model = Ingredient
    fields = ['name', 'amount', 'preparation']
   
    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.recipe
        return context
    
    def get_success_url(self):
        return reverse('add-ingredient', kwargs={'pk': self.object.recipe.id})

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class IngredientUpdate(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = ['name', 'amount', 'preparation']

    def dispatch(self, request, *args, **kwargs):
        self.next = request.POST.get('next', '/')
        self.referer = request.META.get('HTTP_REFERER', '')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe
        context['pk'] = self.object.id
        context['update'] = True
        context['instruction_next'] = 'instruction' in self.referer
        return context

    def get_success_url(self):
        return self.next

class IngredientDelete(LoginRequiredMixin, DeleteView):
    model = Ingredient

    def dispatch(self, request, *args, **kwargs):
        self.next = request.POST.get('next', '/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe
        context['pk'] = self.object.id
        return context

    def get_success_url(self):
        return self.next

class InstructionCreate(LoginRequiredMixin, CreateView):
    model = Instruction
    fields = ['step_number', 'description']
   
    def dispatch(self, request, *args, **kwargs):
        self.recipe = get_object_or_404(Recipe, pk=kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.recipe
        return context

    def get_success_url(self):
        return reverse('add-instruction', kwargs={'pk': self.object.recipe.id})

    def form_valid(self, form):
        form.instance.recipe = self.recipe
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class InstructionUpdate(LoginRequiredMixin, UpdateView):
    model = Instruction
    fields = ['step_number', 'description']

    def dispatch(self, request, *args, **kwargs):
        self.next = request.POST.get('next', '/')
        self.referer = request.META.get('HTTP_REFERER', '')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe
        context['pk'] = self.object.id
        context['update'] = True
        context['instruction_next'] = 'instruction' in self.referer
        return context

    def get_success_url(self):
        return self.next

class InstructionDelete(LoginRequiredMixin, DeleteView):
    model = Instruction

    def dispatch(self, request, *args, **kwargs):
        self.next = request.POST.get('next', '/')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipe'] = self.object.recipe
        context['pk'] = self.object.id
        return context

    def get_success_url(self):
        return self.next