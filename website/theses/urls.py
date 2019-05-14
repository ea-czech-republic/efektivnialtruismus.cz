from django.conf.urls import url
from .views import conversion

theses_urls = [url(r"^conversion/$", conversion, name="conversion")]
