from django.contrib import admin

from .models import Ingredient, Instruction, Recipe

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Instruction)
