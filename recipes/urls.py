from django.urls import path, re_path
from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.home, name="home"),
    path('recipes/create', views.RecipeCreateView.as_view()),
    path("recipes/<slug:the_slug>/edit/", views.RecipeEditView.as_view(), name="edit"),
    path("recipes", views.RecipeList.as_view(), name="recipe"),
    path("recipes/<slug:the_slug>",
         views.RecipeDetail.as_view(),
         name="recipe-detail"),
    path("recipes/<slug:the_slug>/delete/",
         views.RecipeDeleteView.as_view(),
         name="recipe-del"),
]
