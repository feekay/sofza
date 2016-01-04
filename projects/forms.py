from django import forms
from projects.models import Project, Milestone
from multiupload.fields import MultiFileField

class MyForm(forms.Form):
    file = MultiFileField(min_num=0, max_num=5, max_file_size=1024*1024*5, required = False)


class projectForm(forms.ModelForm):
    client = forms.CharField(max_length = 50)
    client_mail = forms.EmailField()
    title = forms.CharField(max_length=50)
    cost = forms.IntegerField()
    estimated_end_date= forms.DateField()
    start_date = forms.DateField()

    class Meta:
        model = Project
        exclude = ['id', 'last_updated', 'completed']

class milestoneForm(forms.ModelForm):
    title = forms.CharField(max_length = 50)
    #Apply widget text area
    description = forms.CharField(max_length = 500, widget=forms.Textarea())
    start_date = forms.DateField()
    deadline = forms.DateField()

    
    class Meta:
        model = Milestone
        widgets = {
            'project': forms.HiddenInput()
        }
        exclude=[]
