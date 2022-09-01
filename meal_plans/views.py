# from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy

from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from meal_plans.models import MealPlan


class MealPlanCreateView(LoginRequiredMixin, CreateView):
    model = MealPlan
    template_name = "meal_plans/new.html"
    fields = ["name", "date", "recipes"]

    # override form_valid; extra step required for saving to db
    def form_valid(self, form):
        # get plan
        meal_plans = form.save(commit=False)
        # set plan owner to logged in user
        meal_plans.owner = self.request.user
        # save meal_plan
        meal_plans.save()
        # save form
        form.save_m2m()
        return redirect("meal_plans_detail", pk=meal_plans.id)


class MealPlanDeleteView(LoginRequiredMixin, DeleteView):
    model = MealPlan
    template_name = "meal_plans/delete.html"
    success_url = reverse_lazy("meal_plans_list")

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanDetailView(LoginRequiredMixin, DetailView):
    model = MealPlan
    template_name = "meal_plans/detail.html"

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanListView(LoginRequiredMixin, ListView):
    model = MealPlan
    template_name = "meal_plans/list.html"
    paginate_by = 10
    # context_object_name = "mealplan_list"

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)


class MealPlanUpdateView(LoginRequiredMixin, UpdateView):
    model = MealPlan
    template_name = "meal_plans/edit.html"
    fields = ["name", "date", "recipes"]

    def get_queryset(self):
        return MealPlan.objects.filter(owner=self.request.user)

    # override form_valid; extra step required for saving to db
    def form_valid(self, form):
        # get plan
        meal_plans = form.save(commit=False)
        # set plan owner to logged in user
        meal_plans.owner = self.request.user
        # save meal_plan
        meal_plans.save()
        # save form
        form.save_m2m()
        return redirect("meal_plans_detail", pk=meal_plans.id)
