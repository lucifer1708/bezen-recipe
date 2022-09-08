from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from .forms import RecipeForm
from .models import Recipe
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Create your views here.


def error_404_view(request, exception):
    return render(request, "404.html")


def error_500_view(request):
    return render(request, "500.html")


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
    success_url = '/my_recipes'
    login_url = '/auth/login/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin,
                       generic.DeleteView):
    model = Recipe
    template_name = 'recipe/recipe_delete.html'
    success_url = '/my_recipes'
    slug_url_kwarg = 'the_slug'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False


class RecipeEditView(LoginRequiredMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "recipe/edit.html"
    success_url = '/my_recipes'
    slug_url_kwarg = 'the_slug'


@login_required()
def my_recipe(request):
    user_recipe = []
    user_recipe = Recipe.objects.filter(author=request.user)
    return render(request=request,
                  template_name='recipe/recipe_user_list.html',
                  context={
                      'user': request.user,
                      'recipes': user_recipe
                  })
