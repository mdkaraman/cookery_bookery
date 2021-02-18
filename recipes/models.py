from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator


class Recipe(models.Model):
    """Model representing a complete recipe"""

    name = models.CharField(
        max_length=200, 
        help_text='Enter a name for this recipe'
        )
    servings = models.PositiveIntegerField(
        help_text='Enter the number of servings this recipe makes',
        validators=[MinValueValidator(1)]
        )
    nota_bene = models.TextField(
        help_text='Add any useful notes, hints or advice for this recipe', 
        null=True,
        blank=True
        )

    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('recipe-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Model representing an ingredient in a recipe."""
    
    recipe = models.ForeignKey(
        Recipe,
        help_text='Choose a recipe to add an ingredient to', 
        on_delete=models.CASCADE
        )
    name = models.CharField(
        max_length=100, 
        help_text='Enter the name of an ingredient (e.g. garlic)'
        )
    amount = models.CharField(
        max_length=20, 
        help_text='Enter the amount to use (e.g. 1/4 tsp.)'
        )
    preparation = models.CharField(
        max_length=100, 
        help_text='Describe this ingredient"s preparation (e.g. finely minced) or leave blank', 
        null=True,
        blank=True
        )

    def __str__(self):
        prep = ', ' + self.preparation if self.preparation else ''
        return '{0} {1}{2}'.format(self.amount, self.name, prep)

class Instruction(models.Model):
    """Model representing a single instruction in a recipe"""

    recipe = models.ForeignKey(
        Recipe,
        help_text='Choose a recipe to add an instruction to', 
        on_delete=models.CASCADE
        )
    step_number = models.PositiveIntegerField(
        help_text='Enter the order number for this instruction (e.g. step 1, step 2, etc.)',
        validators=[MinValueValidator(1)]
        )
    description = models.TextField(
        help_text="Add an instruction to the recipe"
        )

    class Meta:
        ordering = ['recipe', 'step_number']

    def __str__(self):
        return '{0}: Step {1}'.format(self.recipe.name, self.step_number)