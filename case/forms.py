from django import forms
from case.models import case, Task , Document#, Report
from account.models import UserProfile


class Reg_Case(forms.ModelForm):
    case_number = forms.IntegerField()
    investigation_head = forms.ModelChoiceField(queryset= UserProfile.objects.filter(designation = 'investigation head'),widget= forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = case
        fields = ('case_number','investigation_head')

class New_Case(forms.ModelForm):
    case_info = forms.CharField(widget= forms.Textarea(attrs={'class':'form-control' }))
    deadline = forms.DateField(widget= forms.TextInput(attrs={'class':'form-control input-rounded', 'placeholder':'set deadline', 'id':'mdate'}))
    members = forms.ModelMultipleChoiceField(queryset= UserProfile.objects.filter(designation = 'member'),widget=forms.SelectMultiple(attrs={'class':'form-control', 'id':'sel2'}))
    class Meta:
        model = case
        fields = ('case_info','deadline','members')

Choices = (
    ('Under Investigation','Under Investigation'),
    ('Completed','Completed'),
    ('Cancelled', 'Cancelled'),
)
class Update_Status(forms.ModelForm):
    status = forms.ChoiceField(choices= Choices,widget= forms.Select(attrs={'class':'custom-select'}))
    class Meta:
        model = case
        fields = ('status',)

class Reg_Task(forms.ModelForm):
    case_number = forms.IntegerField()
    task_number = forms.IntegerField()
    task_info = forms.CharField(widget= forms.Textarea(attrs={'class':'form-control' }))
    deadline = forms.DateField(widget= forms.TextInput(attrs={'class':'form-control input-rounded', 'placeholder':'set deadline', 'id':'mdate'}))
    task_member = forms.ModelChoiceField(queryset= UserProfile.objects.filter(designation = 'member'),widget=forms.Select(attrs={'class':'form-control'}))
    task_case = forms.ModelChoiceField(queryset= case.objects.all(),widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = Task
        fields = ('case_number','task_number','task_info','deadline','task_member','task_case')

Task_Choices = (
    ('Ongoing','Ongoing'),
    ('Completed','Completed'),
    ('Cancelled', 'Cancelled'),
)
class Update_Task_Status(forms.ModelForm):
    task_status = forms.ChoiceField(choices= Task_Choices,widget= forms.Select(attrs={'class':'custom-select'}))
    class Meta:
        model = case
        fields = ('task_status',)

"""
class Report_Form(forms.ModelForm):
    report = forms.CharField(required = False, widget= forms.Textarea(attrs={'class':'form-control' }))
    class Meta:
        model = Report
        fields=('report',)
"""
#NLP
class DocumentForm(forms.ModelForm):
    model = Document
    file1 = forms.FileField(
    label='Select a file',
    help_text='max. 42 megabytes'
    )
    csvfile1 = forms.FileField(
    label='Select a file',
    help_text='max. 42 megabytes'
    )
    audio1 = forms.FileField(
    label='Select a file',
    help_text='max. 42 megabytes'
    )
    class Meta:
        model = Document
        fields = ('unq','file1','csvfile1' , 'audio1' , 'url1')
