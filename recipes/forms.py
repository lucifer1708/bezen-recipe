from django import forms
from .models import Recipe
from ckeditor.widgets import CKEditorWidget


class RecipeForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'thumbnail', 'content']
