from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('all-recipes/', views.RecipeListView.as_view(), name='all-recipes'),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('my-recipes/<int:pk>', views.MyRecipesListView.as_view(), name='my-recipes'),
    path('submit-recipe/create', views.RecipeCreate.as_view(), name='create-recipe'),
    path('submit-recipe/<int:pk>/add-ingredient', views.IngredientCreate.as_view(), name='add-ingredient'),
    path('submit-recipe/<int:pk>/add-instruction', views.InstructionCreate.as_view(), name='add-instruction'),
    path('submit-recipe/<int:pk>/update_recipe', views.RecipeUpdate.as_view(), name='update-recipe'),
    path('submit-recipe/<int:pk>/update_ingredient', views.IngredientUpdate.as_view(), name='update-ingredient'),
    path('submit-recipe/<int:pk>/update_instruction', views.InstructionUpdate.as_view(), name='update-instruction'),
    path('recipe/<int:pk>/delete', views.RecipeDeleteView.as_view(), name='delete-recipe'),
    path('submit-recipe/<int:pk>/delete_ingredient', views.IngredientDelete.as_view(), name='delete-ingredient'),
    path('submit-recipe/<int:pk>/delete_instruction', views.InstructionDelete.as_view(), name='delete-instruction'),
]
