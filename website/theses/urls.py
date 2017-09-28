from django.conf.urls import include, url
from .views import feedback_form

theses_urls = [
    url(r'^feedback/$', feedback_form, name='feedback'),
]