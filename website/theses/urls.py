from django.conf.urls import url
from .views import conversion, submit_to_newsletter, ask_as_anything

theses_urls = [
    url(r"^conversion/$", conversion, name="conversion"),
    url(r"^newsletter/$", submit_to_newsletter, name="newsletter"),
    url(r"^ask_us_anything/$", ask_as_anything, name="ask_us_anything"),
]
