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
