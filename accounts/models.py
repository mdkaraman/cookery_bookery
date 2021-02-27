import recipes.models
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Use string argument for Recipe model to prevent circular import error
    favorite_recipes = models.ManyToManyField("recipes.Recipe")
