from django import forms

class FeedbackForm(forms.Form):
    contact_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                                    'placeholder': 'Your email'}))
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'What would you like to tell us?'})
    )


class SimpleContactForm(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your name',
                                                                                'class': 'form-control'}))
    contact_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                                   'placeholder': 'Your email'}))
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'What would you like to tell us?'})
    )


class InterestsForm(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your name',
                                                                                'class': 'form-control'}))
    contact_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                                   'placeholder': 'Your email'}))
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'Do you have anything else you would like to tell us?'})
    )

    course_and_university = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Course and University'})
    )

    deadline = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'DD-MM-YYYY'}))

    thesis_title = forms.CharField(required=False)


class ProposalForm(forms.Form):
    contact_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Your name',
                                                                                'class': 'form-control'}))
    contact_email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                                   'placeholder': 'Your email'}))
    organisation = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'placeholder': 'Your organisation'})
    )
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Thesis title',
                                                                         'class': 'form-control'}))
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'Thesis description'})
    )

    why_important = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'Why is it important?'})
    )

    sources = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'Sources'})
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control',
                                     'placeholder': 'Is there anything else you '
                                                    'would like to inform us about?'})
    )


def get_discipline_choices():
    from theses.models import ThesisDiscipline
    discs = ThesisDiscipline.objects.all()
    return [(None, None)] + [(x.name, x.name) for x in discs]


class DisciplineSelect(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DisciplineSelect, self).__init__(*args, **kwargs)
        self.fields['discipline'] = forms.ChoiceField(choices=get_discipline_choices())
        self.fields['discipline'].widget.attrs['onchange'] = 'this.form.submit()'
        self.fields['discipline'].widget.attrs['class'] = 'custom-select'
