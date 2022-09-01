from django.urls import path

from meal_plans.views import (
    MealPlanListView,
    MealPlanDeleteView,
    MealPlanDetailView,
    MealPlanCreateView,
    MealPlanUpdateView,
)

urlpatterns = [
    path("", MealPlanListView.as_view(), name="meal_plans_list"),
    path("<int:pk>/", MealPlanDetailView.as_view(), name="meal_plans_detail"),
    path(
        "<int:pk>/delete/",
        MealPlanDeleteView.as_view(),
        name="meal_plans_delete",
    ),
    path("create/", MealPlanCreateView.as_view(), name="meal_plans_new"),
    path(
        "<int:pk>/edit/", MealPlanUpdateView.as_view(), name="meal_plans_edit"
    ),
]
