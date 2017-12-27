from django.conf.urls import url
from .views import feedback_form, conversion

theses_urls = [
    url(r'^feedback/$', feedback_form, name='feedback'),
    url(r'^conversion/$', conversion, name='conversion'),
]
