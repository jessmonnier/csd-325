from django.forms import ModelForm
from django import forms
from .models import Task, Category

# Makes a more user friendly way of selecting a date/time for a task
class DateTimePickerInput(forms.DateTimeInput):
    input_type = 'datetime-local'

# Make the input form used to display & edit/submit tasks
# The attrs class form-control thing is for CSS styling
class FormTask(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'due_date': DateTimePickerInput(attrs={'class': 'form-control'})
        }

# Make the input form used to display and edit/submit task categories
class FormCategory(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'})
        }