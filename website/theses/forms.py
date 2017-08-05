from django import forms
import datetime


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your name',
                                                                                'class': 'form-control'}))
    contact_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                                   'placeholder': 'Your email'}))
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'Content'})
    )

    course_and_university = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'Content'})
    )

    deadline = forms.DateField(initial=datetime.date.today,
                               widget=forms.widgets.DateInput(
                                   attrs={'type': 'date', 'id': 'deadline-picker'}))
