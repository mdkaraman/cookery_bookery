from django.forms import ModelForm

from .models import Ingredient, Instruction, Recipe


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ["name", "servings", "nota_bene"]
    

class IngredientForm(ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "amount", "preparation"]


class InstructionForm(ModelForm):
    class Meta:
        model = Instruction
        fields = ["step_number", "description"]
