from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from wagtail.admin.utils import send_mail
from textwrap import dedent

THESES_MAILS = ["david@effectivethesis.com"]


def conversion(request, origin_url, title):
    context = {"origin_url": origin_url, "title": title}
    return render(request, "theses/conversion.html", context)


def coaching_conversion(request):
    return render(request, "theses/coaching_conversion.html")


def build_mail_content_contact(contact_name, contact_email, message):
    return dedent(
        f"""
    Name: {contact_name},
    Contact email: {contact_email},

    --------Message--------
    {message}
    """)


def dejsonize(content):
    return {x['name']: x['value']
            for x in json.loads(content)
            }


@csrf_exempt
def submit_to_newsletter(request):
    print(request.is_ajax())
    if request.is_ajax():
        if request.method == 'POST':
            form_data = dejsonize(request.body.decode())
            contact_name = form_data['contact_name']
            contact_email = form_data['contact_email']
            send_mail(
                "Contacting using Contact Form in Footer",
                build_mail_content_contact(contact_name, contact_email, "Interest in newsletter"),
                THESES_MAILS,  # recipient email
                contact_email,
            )
            return HttpResponse("Thank you for your interest!")
    else:
        return HttpResponse("Something went wrong when submitting to newsletter")


@csrf_exempt
def ask_as_anything(request):
    if request.is_ajax():
        if request.method == 'POST':
            form_data = dejsonize(request.body.decode())
            contact_name = form_data['contact_name']
            contact_email = form_data['contact_email']
            text = form_data['contact_email']
            send_mail(
                "Contacting using Contact Form on About us",
                build_mail_content_contact(contact_name, contact_email, text),
                THESES_MAILS,  # recipient email
                contact_email,
            )
            return HttpResponse("Thank you for your question! We'll get back to you as soon as possible.")
    else:
        return HttpResponse("Something went wrong when contacting us.")
