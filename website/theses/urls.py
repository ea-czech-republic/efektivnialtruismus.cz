from django.conf.urls import url
from .views import conversion, submit_to_newsletter, ask_us_anything

theses_urls = [
    url(r"^conversion/$", conversion, name="conversion"),
    url(r"^newsletter/$", submit_to_newsletter, name="newsletter"),
    url(r"^ask_us_anything/$", ask_us_anything, name="ask_us_anything"),
]
