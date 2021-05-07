from .models import *
from django import forms
from froala_editor.widgets import FroalaEditor



class JobForm(forms.ModelForm):
    class Meta:
        model = InternalJobPosting
        fields = ['job_description'] 
        #content = forms.CharField(widget=FroalaEditor)
