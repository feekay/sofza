from django import forms
from mysite.models import eMail

class mailForm(forms.ModelForm):
    
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'required': ''}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'required': ''}))
    class Meta:
        model = eMail
        exclude = []
