from croppie.fields import CroppieField
from django import forms
from .models import *

from client_side_image_cropping import ClientsideCroppingWidget

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        widgets = {
            'image': ClientsideCroppingWidget(
                width=400,
                height=600,
                preview_width=100,
                preview_height=150,
            )
        }


class AddForm(forms.Form):
    photo = CroppieField(options={
            'viewport': {
                'width': 120,
                'height': 140,
            },
            'boundary': {
                'width': 200,
                'height': 220,
            },
            'showZoomer': True,
        },)