from django.urls import path

from recipes.views import (
    RecipeCreateView,
    RecipeDeleteView,
    RecipeUpdateView,
    log_rating,
    RecipeDetailView,
    RecipeListView,
    ShoppingItemListView,
    ShoppingItemDelete,
    ShoppingItemCreate,
)

urlpatterns = [
    path("", RecipeListView.as_view(), name="recipes_list"),
    path("<int:pk>/", RecipeDetailView.as_view(), name="recipe_detail"),
    path("<int:pk>/delete/", RecipeDeleteView.as_view(), name="recipe_delete"),
    path("new/", RecipeCreateView.as_view(), name="recipe_new"),
    path("<int:pk>/edit/", RecipeUpdateView.as_view(), name="recipe_edit"),
    path("<int:recipe_id>/ratings/", log_rating, name="recipe_rating"),
    path(
        "shopping_items/",
        ShoppingItemListView.as_view(),
        name="shoppingitem_list",
    ),
    path(
        "shopping_items/delete/",
        ShoppingItemDelete,
        name="shoppingitem_delete",
    ),
    path(
        "shopping_items/create/",
        ShoppingItemCreate,
        name="shoppingitem_create",
    ),
]
