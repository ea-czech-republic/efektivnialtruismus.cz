from .forms import FeedbackForm
from django.http import JsonResponse
from django.shortcuts import redirect
from textwrap import dedent
from wagtail.wagtailadmin.utils import send_mail

THESES_MAILS = ['theses@efektivni-altruismus.cz']


def build_mail_content(uri, data):
    return dedent("""
    URL: {thesis_uri}
    Contact email: {contact_email},

    --------Message--------
    {content}
    """.format(thesis_uri=uri, **data))


def feedback_form(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.clean()

            contact_email = form.cleaned_data['contact_email']
            if contact_email is None:
                contact_email = THESES_MAILS[0]

            mail_content = build_mail_content(request.build_absolute_uri(), form.cleaned_data)
            send_mail('Feedback',
                      mail_content,
                      THESES_MAILS,
                      contact_email
                      )
            #return JsonResponse({'message': 'Thank you for your interest! '
            #                    'We will let get back to you soon!'})
            return redirect(request.META['HTTP_REFERER'])
        else:
            return JsonResponse({'message': 'Sorry, submitting your form was not '
                                            'successful. Please use our contact page.'})
    else:
        return JsonResponse({'message': 'Different than POST message is not allowed'})
