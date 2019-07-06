from django.conf.urls import url
from .views import conversion, submit_to_newsletter

theses_urls = [
    url(r"^conversion/$", conversion, name="conversion"),
    url(r"^newsletter/$", submit_to_newsletter, name="newsletter")
]
