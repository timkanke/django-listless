from django import forms
from django.forms import ModelForm, RadioSelect, TextInput, Textarea
from crispy_forms.helper import FormHelper
from .models import Image, Item


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'photo']


class ItemFilterForm(forms.Form):
    author = forms.CharField()
    title = forms.CharField()
    publish = forms.BooleanField()


class ItemUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Item
        fields = (
            'author',
            'title',
            'publish',
        )

        widgets = {
            'author': TextInput(attrs={'class': 'form-control'}),
        }
