from attr import field
from django import forms
from lists.models import Item


EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.Form):
    class Meta:
        model = Item
        field = ('text',)
        widgets = {
            'test': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg'
            }),
        }
        error_message = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }
