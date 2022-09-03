from django import template

register = template.Library()


def resize_to(ingredient, servings_input):
    servings = ingredient.recipe.servings
    amount = ingredient.amount

    if servings is not None and servings_input is not None:
        ratio = int(servings_input) / servings
        return amount * ratio
    else:
        return amount


register.filter(resize_to)
