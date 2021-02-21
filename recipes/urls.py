from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('all-recipes/', views.RecipeListView.as_view(), name='all-recipes'),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('submit-recipe/create', views.RecipeCreate.as_view(), name='create-recipe'),
    path('submit-recipe/<int:pk>/add-ingredient', views.IngredientCreate.as_view(), name='add-ingredient'),
    path('submit-recipe/<int:pk>/add-instruction', views.InstructionCreate.as_view(), name='add-instruction')
]
