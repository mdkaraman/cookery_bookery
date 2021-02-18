from django.db import models

class Recipe(models.Model):
    """Model representing a complete recipe"""

    name = models.CharField(
        max_length=200, 
        help_text='Enter a name for this recipe'
        )
    servings = models.IntegerField(
        help_text='Enter the number of servings this recipe makes'
        )
    nota_bene = models.TextField(
        help_text='Add any useful notes, hints or advice for this recipe', 
        null=True
        )

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    """Model representing an ingredient in a recipe."""

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
        null=True
        )

    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE
        )

    def __str__(self):
        return '{0} {1}, {2}'.format(self.amount, self.name, self.preparation)

class Instruction(models.Model):
    """Model representing a single instruction in a recipe"""

    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE
        )
    description = models.TextField(
        help_text="Add a step to the recipe's instructions"
        )

    def __str__(self):
        return '{0}...'.format(self.description[:100])