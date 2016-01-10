from django import forms
from projects.models import Project, Milestone, Staff
from django.contrib.auth.models import User
from multiupload.fields import MultiFileField
from django.forms.extras.widgets import SelectDateWidget


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields= ['first_name','last_name','username', 'email', 'password']

class StaffForm(forms.ModelForm):
    picture = forms.FileField(required=False)
    class Meta:
        model= Staff
        exclude = ['user']

class MyForm(forms.Form):
    file = MultiFileField(min_num=0, max_num=5, max_file_size=1024*1024*5, required = False)
   

class projectForm(forms.ModelForm):
    CHOICES = (('$', "Dollar"),(u'\u00A3',"Pound"),(u'\u20AC', "Euro"))
    client = forms.CharField(max_length = 50, label= "Client Name", widget=forms.TextInput(attrs={'required': ''}))
    client_mail = forms.EmailField(widget=forms.EmailInput(attrs={'required': ''}))
    title = forms.CharField(max_length=50, label = "Project Title", widget=forms.TextInput(attrs={'required': ''}))
    pay_type = forms.ChoiceField(choices = CHOICES, label="Payment Currency", initial='', widget=forms.Select(), required=True)
    estimated_end_date= forms.DateField(widget=SelectDateWidget())
    start_date = forms.DateField(widget=SelectDateWidget())

    class Meta:
        model = Project
        exclude = ['id', 'cost', 'last_updated', 'completed', 'revenue', 'success']

class milestoneForm(forms.ModelForm):
    title = forms.CharField(max_length = 50, label ="Task", widget=forms.TextInput(attrs={'required': ''}))
    description = forms.CharField(max_length = 500, widget=forms.Textarea(attrs={'required': ''}))
    cost = forms.IntegerField(widget=forms.NumberInput(attrs={'required': '', 'min':'0', 'onkeypress':'return event.charCode >= 48 && event.charCode <= 57'}))
    start_date = forms.DateField(widget=SelectDateWidget())
    deadline = forms.DateField(widget=SelectDateWidget())


    class Meta:
        model = Milestone
        widgets = {
            'project': forms.HiddenInput()
        }
        exclude=['url_id', 'completed', 'success', 'paid']

