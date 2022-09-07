from django.shortcuts import render
from django.views import generic
from .forms import RecipeForm
from .models import Recipe
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def home(request):
    return render(request, 'home.html')


class RecipeList(generic.ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipe/recipe_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(title__icontains=query) | Q(ingredients__icontains=query))
        else:
            object_list = self.model.objects.all()
        return object_list


class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name = 'recipe/recipe_detail.html'
    context_object_name = 'recipe'
    slug_url_kwarg = 'the_slug'


class RecipeCreateView(LoginRequiredMixin, generic.CreateView):
    form_class = RecipeForm
    template_name = "recipe/create.html"
    success_url = reverse_lazy('user-recipe-list')
    login_url = '/auth/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                       generic.DeleteView):
    model = Recipe
    template_name = 'recipe/recipe_delete.html'
    success_url = '/'
    slug_url_kwarg = 'the_slug'


class RecipeEditView(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipe/edit.html"
    success_url = reverse_lazy('user-recipe-list')
    slug_url_kwarg = 'the_slug'


class RecipeUserList(generic.ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = 'recipe/recipe_user_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(
                Q(title__icontains=query) | Q(ingredients__icontains=query))
        else:
            object_list = self.model.objects.all()
        return object_list
