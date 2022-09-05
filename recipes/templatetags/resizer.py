from django import template

register = template.Library()


def resize_to(ingredient, servings_input):
    # Get the number of servings from the ingredient's
    # recipe using the ingredient.recipe.servings
    # properties
    servings = ingredient.recipe.servings

    # Get ingredient's amount
    amount = ingredient.amount

    # If the servings from the recipe is not None
    #   and the value of target is not None
    if servings is not None and servings_input is not None:
        # try
        #   calculate the ratio of target over
        #       servings
        #   return the ratio multiplied by the
        #       ingredient's amount
        try:
            ratio = int(servings_input) / servings
            return ratio * amount
        # catch a possible error
        #   pass
        except ValueError:
            pass

    # return the original ingredient's amount since
    #   nothing else worked
    else:
        return amount

    print("value:", ingredient)
    print("arg:", servings_input)
    return "resize done"


register.filter(resize_to)
