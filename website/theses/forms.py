from django import forms


class SimpleContactForm(forms.Form):
    contact_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Your name", "class": "form-control"}
        ),
    )
    contact_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your email"}
        ),
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "What would you like to tell us?",
            }
        ),
    )


class InterestsForm(forms.Form):
    contact_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Your name", "class": "form-control"}
        ),
    )
    contact_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your email"}
        ),
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Which ideas/topics have you considered so far if any?",
            }
        ),
    )

    course_and_university = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Course and University"}
        )
    )

    deadline = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "DD-MM-YYYY"}
        )
    )

    find_out_website = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "How did you find out about this website?",
                "rows": 5,
            }
        ),
    )

    thesis_title = forms.CharField(required=False)


class CoachingForm(forms.Form):
    contact_name = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Your name", "class": "form-control"}
        ),
    )
    contact_email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Your email"}
        ),
    )
    university = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Course and University"}
        ),
    )

    choices_seniority = ["Undergraduate", "Masters", "PhD", "post-PhD"]
    seniority = forms.ChoiceField(
        choices=zip(choices_seniority, choices_seniority),
    )

    career = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Briefly describe your career plans (e.g. Do you "
                               "want to become top reseacher? Do you know the sector "
                               "or type of work that you would like to do after you graduate?)",
                "rows": 5,
            }
        ),
    )

    preferences = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Which ideas/topics have you considered so far if any?",
                "rows": 5,
            }
        ),
    )

    read_above = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Suppose someone would give you 100.000 USD to distribute it for charitable reasons. How would you decide how to distribute it?",
                "rows": 5,
            }
        ),
    )

    deadline = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "When is your deadline for having a topic chosen?",
            }
        )
    )

    deadline_submit = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "When is your deadline for submitting your thesis?",
            }
        )
    )

    requirements = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Any requirements we should be aware of? Do you have to use particular methodology? Do you have some budget available? Does your supervisor have some requirements (if you already have a supervisor)?",
                "rows": 5,
            }
        ),
    )

    cv_url = forms.URLField(
        required=False,
        widget=forms.URLInput(
            attrs={
                "class": "form-control",
                "placeholder": "Send us link to your CV or other summary of your (research) experience",
            }
        )
    )

    find_out_website = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "How did you find out about this website?",
                "rows": 5,
            }
        ),
    )

    anything_else = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Anything else you would like to tell us?",
                "rows": 5,
            }
        ),
    )


def get_discipline_choices():
    from theses.models import ThesisDiscipline

    discs = ThesisDiscipline.objects.all()
    return [(None, None)] + [(x.name, x.name) for x in discs]
