from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('all-recipes/', views.RecipeListView.as_view(), name='all-recipes'),
    path('recipe/<int:pk>', views.RecipeDetailView.as_view(), name='recipe-detail'),
    path('submit-recipe/', views.user_submit_recipe, name='submit-recipe'),
    path('submit-recipe/<int:pk>/add-ingredient', views.user_add_ingredient, name='add-ingredient'),
    path('submit-recipe/<int:pk>/add-instruction', views.user_add_instruction, name='add-instruction')
]
