from django.db import models
from django.conf import settings

USER_MODEL = settings.AUTH_USER_MODEL


class MealPlan(models.Model):
    name = models.CharField(max_length=120)
    date = models.DateField(auto_now_add=False, null=True)
    owner = models.ForeignKey(
        USER_MODEL,
        related_name="meal_plans",
        on_delete=models.CASCADE,
        null=True,
    )
    recipes = models.ManyToManyField(
        "recipes.Recipe", related_name="meal_plans"
    )

    def __str__(self):
        return self.name
