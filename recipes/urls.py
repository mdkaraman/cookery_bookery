from django.urls import path

from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("all/", views.RecipeListView.as_view(), name="all-recipes"),
    path("<int:pk>", views.RecipeDetailView.as_view(), name="recipe-detail"),
    path("my-recipes/", views.MyRecipesListView.as_view(), name="my-recipes"),
    path("my-favorites/", views.MyFavoritesListView.as_view(), name="my-favorites"),
    path("submit/create/", views.RecipeCreate.as_view(), name="create-recipe"),
    path(
        "submit/<int:pk>/add-ingredient",
        views.IngredientCreate.as_view(),
        name="add-ingredient",
    ),
    path(
        "submit/<int:pk>/add-instruction",
        views.InstructionCreate.as_view(),
        name="add-instruction",
    ),
    path(
        "submit/<int:pk>/update_recipe",
        views.RecipeUpdate.as_view(),
        name="update-recipe",
    ),
    path(
        "submit/<int:pk>/update_ingredient",
        views.IngredientUpdate.as_view(),
        name="update-ingredient",
    ),
    path(
        "submit/<int:pk>/update_instruction",
        views.InstructionUpdate.as_view(),
        name="update-instruction",
    ),
    path(
        "recipe/<int:pk>/delete", views.RecipeDeleteView.as_view(), name="delete-recipe"
    ),
    path(
        "submit/<int:pk>/delete_ingredient",
        views.IngredientDelete.as_view(),
        name="delete-ingredient",
    ),
    path(
        "submit/<int:pk>/delete_instruction",
        views.InstructionDelete.as_view(),
        name="delete-instruction",
    ),
]
