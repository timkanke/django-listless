from django.forms import ModelForm, RadioSelect, TextInput, Textarea
from crispy_forms.helper import FormHelper
from .models import Item


class ItemUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()

    class Meta:
        model = Item
        fields = ('author',
                  'title',
                  'publish',
                  )

        widgets = {
            'author': TextInput(attrs={'class': 'form-control'}),
        }
