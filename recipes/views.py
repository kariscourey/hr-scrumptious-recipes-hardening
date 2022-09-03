from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from recipes.forms import RatingForm


# from recipes.forms import RecipeForm
from recipes.models import Recipe, ShoppingItem, Ingredient

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError


def log_rating(request, recipe_id):
    if request.method == "POST":
        form = RatingForm(request.POST)
        try:
            if form.is_valid():
                rating = form.save(commit=False)
                rating.recipe = Recipe.objects.get(pk=recipe_id)
                rating.save()
            return redirect("recipe_detail", pk=recipe_id)
        except Recipe.DoesNotExist:
            return redirect("recipes_list")


class RecipeListView(ListView):
    model = Recipe
    template_name = "recipes/list.html"
    paginate_by = 2

    # def get_queryset(self):
    #     # Get the normal queryset
    #     queryset = super().get_queryset()

    #     print("this is the queryset \n")

    #     # Print it to see what's in it
    #     print(queryset)

    #     # Return it like nothing ever happened
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     # Let the parent class get the context for
    #     # the actual Post for its detail
    #     context = super().get_context_data(**kwargs)

    #     # Print it out to see what's in it
    #     from pprint import pprint

    #     pprint(context)

    #     # Return it like nothing ever happened
    #     return context


class RecipeDetailView(DetailView):
    model = Recipe
    template_name = "recipes/detail.html"

    # # Get the value from the
    # # request.POST dictionary using the "get" method
    # servings_input = 3  # Recipe.request.GET.get("servings_input")

    # # # Multiply values of ingredient.amount by servings_input
    # for recipe in Recipe.objects.all():
    #     for ing in recipe.ingredients.all():
    #         ing.amount *= servings_input

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm()
        # context["shoppingitem_list"] = self.request.user.shoppingitem.all()

        # Create a new empty list and assign it to a variable
        foods = []

        # For each item in the user's shopping items, which we
        # can access through the code
        # self.request.user.shopping_items.all()
        for item in self.request.user.shoppingitem.all():
            # Add the shopping item's food to the list
            foods.append(item.food_item)

        # Put that list into the context
        context["food_in_shopping_list"] = foods

        # The self.request.GET property is a dictionary
        # Get the value out of there associated with the
        #   key "servings"
        # Store in the context dictionary with the key
        #   "servings"
        # context["servings"] = self.request.GET("servings_input")

        return context

    # def get_queryset(self):
    #     # Get the normal queryset
    #     queryset = super().get_queryset()

    #     print("this is the queryset \n")

    #     # Print it to see what's in it
    #     print(queryset)

    #     # Return it like nothing ever happened
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     # Let the parent class get the context for
    #     # the actual Post for its detail
    #     context = super().get_context_data(**kwargs)

    #     # Print it out to see what's in it
    #     from pprint import pprint

    #     pprint(context)

    #     # Return it like nothing ever happened
    #     return context


class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = "recipes/new.html"
    fields = ["name", "description", "servings", "image"]
    success_url = reverse_lazy("recipes_list")

    # override form_valid
    def form_valid(self, form):
        # get logged in user
        user = self.request.user
        # set author attribute of recipe to logged in user
        form.instance.author = user
        return super().form_valid(form)


class RecipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipe
    template_name = "recipes/edit.html"
    fields = ["name", "description", "servings", "image"]
    success_url = reverse_lazy("recipes_list")

    # override form_valid
    def form_valid(self, form):
        # get logged in user
        user = self.request.user
        # set author attribute of recipe to logged in user
        form.instance.author = user
        return super().form_valid(form)

    # def get_queryset(self):
    #     # Get the normal queryset
    #     queryset = super().get_queryset()

    #     print("this is the queryset \n")

    #     # Print it to see what's in it
    #     print(queryset)

    #     # Return it like nothing ever happened
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     # Let the parent class get the context for
    #     # the actual Post for its detail
    #     context = super().get_context_data(**kwargs)

    #     # Print it out to see what's in it
    #     from pprint import pprint

    #     pprint(context)

    #     # Return it like nothing ever happened
    #     return context


class RecipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipe
    template_name = "recipes/delete.html"
    success_url = reverse_lazy("recipes_list")

    # super cool if would only allow user who owns recipe to edit/delete


class ShoppingItemListView(ListView):
    model = ShoppingItem
    template_name = "shoppingitem_list.html"
    paginate_by = 10

    def get_queryset(self):
        return ShoppingItem.objects.filter(author=self.request.user)


@require_http_methods(["POST"])
@login_required(login_url="registration/login")
def ShoppingItemCreate(request):

    # Get the value for the "ingredient_id" from the
    # request.POST dictionary using the "get" method
    ingredient_id = request.POST.get("ingredient_id")

    # Get the specific ingredient from the Ingredient model
    # using the code
    # Ingredient.objects.get(id=the value from the dictionary)
    ingredient = Ingredient.objects.get(id=ingredient_id)

    # Get the current user which is stored in request.user
    user = request.user

    try:
        # Create the new shopping item in the database
        # using ShoppingItem.objects.create(
        #   food_item= the food item on the ingredient,
        #   user= the current user
        # )
        ShoppingItem.objects.create(
            food_item=ingredient.food,
            author=user,
        )
    except IntegrityError:
        pass

    # Go back to the recipe page with a redirect
    # to the name of the registered recipe detail
    # path with code like this
    # return redirect(
    #     name of the registered recipe detail path,
    #     pk=id of the ingredient's recipe
    # )
    return redirect("recipe_detail", pk=ingredient.recipe.id)


@require_http_methods(["POST"])
@login_required(login_url="registration/login")
def ShoppingItemDelete(request):

    # Get the current user which is stored in request.user
    user = request.user

    # Delete all of the shopping items for the user
    # using code like
    # ShoppingItem.objects.filter(user=the current user).delete()
    ShoppingItem.objects.filter(author=user).delete()

    # Go back to the shopping item list with a redirect
    # to the name of the registered shopping item list
    # path with code like this
    # return redirect(
    #     name of the registered shopping item list path
    # )
    return redirect("shoppingitem_list")
