from django.forms import ModelForm

from .models import Ingredient, Instruction, Recipe


class RecipeForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'input'})
        self.fields['description'].widget.attrs.update({'class': 'textarea', 'rows': '3'})
        self.fields['servings'].widget.attrs.update({'class': 'input'})
        self.fields['nota_bene'].widget.attrs.update({'class': 'textarea', 'rows': '8'})
 
    class Meta:
        model = Recipe
        fields = ["name", "description","servings", "nota_bene"]
    

class IngredientForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'input'})
        self.fields['amount'].widget.attrs.update({'class': 'input'})
        self.fields['preparation'].widget.attrs.update({'class': 'input'})

    class Meta:
        model = Ingredient
        fields = ["name", "amount", "preparation"]


class InstructionForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['step_number'].widget.attrs.update({'class': 'input'})
        self.fields['description'].widget.attrs.update({'class': 'textarea', 'rows': '10'})
    
    class Meta:
        model = Instruction
        fields = ["step_number", "description"]
