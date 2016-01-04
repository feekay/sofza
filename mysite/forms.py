from django import forms
from mysite.models import eMail

class mailForm(forms.ModelForm):
    
    name = forms.CharField(required=True)
    email = forms.EmailField()
    class Meta:
        model = eMail
        exclude = []
