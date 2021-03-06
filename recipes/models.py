import accounts.models
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse


class Recipe(models.Model):
    """Model representing a complete recipe."""

    name = models.CharField(max_length=200, help_text="Enter a name for this recipe")
    description = models.TextField(
        help_text="Describe your recipe in a sentence or two."
    )
    servings = models.PositiveIntegerField(
        help_text="Enter the number of servings this recipe makes",
        validators=[
            MinValueValidator(
                1, message="Your recipe needs to make at least 1 serving!"
            )
        ],
    )
    nota_bene = models.TextField(
        help_text="Add any useful notes, hints or advice for this recipe",
        verbose_name="N.B.",
        null=True,
        blank=True,
    )

    # Use string argument for User model to prevent circular import error
    author = models.ForeignKey(
        "accounts.User", on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        return reverse("recipe-detail", args=[str(self.id)])

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Model representing an ingredient in a recipe."""

    recipe = models.ForeignKey(
        Recipe,
        help_text="Choose a recipe to add an ingredient to",
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=100, help_text="Enter the name of an ingredient (e.g. garlic)"
    )
    amount = models.CharField(
        max_length=20, help_text="Enter the amount to use (e.g. 1/4 tsp.)"
    )
    preparation = models.CharField(
        max_length=100,
        help_text="Describe this ingredient's preparation (e.g. finely minced) or leave blank",
        null=True,
        blank=True,
    )

    def __str__(self):
        prep = ", " + self.preparation if self.preparation else ""
        return "{0} {1}{2}".format(self.amount, self.name, prep)


class Instruction(models.Model):
    """Model representing a single instruction in a recipe."""

    recipe = models.ForeignKey(
        Recipe,
        help_text="Choose a recipe to add an instruction to",
        on_delete=models.CASCADE,
    )
    step_number = models.PositiveIntegerField(
        help_text="Enter the step number for this instruction (e.g. step 1)",
        validators=[
            MinValueValidator(
                1, message="Your step numbers should be greater than or equal to 1!"
            )
        ],
        verbose_name="Step",
    )
    description = models.TextField(
        help_text="Describe this step's instructions", verbose_name="Instruction"
    )

    class Meta:
        ordering = ["recipe", "step_number"]

    def __str__(self):
        return "{0}: Step {1}".format(self.recipe.name, self.step_number)
