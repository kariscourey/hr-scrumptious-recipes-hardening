from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin


from recipes.forms import RatingForm


# from recipes.forms import RecipeForm
from recipes.models import Recipe


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["rating_form"] = RatingForm()
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
    fields = ["name", "description", "image"]
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
    fields = ["name", "description", "image"]
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
