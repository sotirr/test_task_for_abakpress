from django.forms import ModelForm

from .models import Page


class CreatePageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['name', 'head', 'content']


class EditPageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['head', 'content']