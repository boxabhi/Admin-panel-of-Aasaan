from .models import *
from django import forms
from froala_editor.widgets import FroalaEditor



class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['content'] 
        #content = forms.CharField(widget=FroalaEditor)
