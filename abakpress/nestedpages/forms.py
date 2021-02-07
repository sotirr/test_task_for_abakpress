from django.forms import ModelForm

from .models import Page


class CreatePageForm(ModelForm):
    ''' forms for creating page '''
    class Meta:
        model = Page
        fields = ['name', 'head', 'content']


class EditPageForm(ModelForm):
    ''' forms for editing page '''
    class Meta:
        model = Page
        fields = ['head', 'content']
