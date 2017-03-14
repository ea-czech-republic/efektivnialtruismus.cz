# efektivnialtruismus.cz on Wagtail

This page is for efektivni-altruismus.cz. It is based on Python `wagtail` CMS.

It is also rewritten from scratch using Bootstrap 4.

The choice of the frameworks `boostrap` and `wagtail` is based on ease of use,
since there will be probably often a change in who manage the site. Both
have strong community and documentation. 

# Why to move?
1. current solution is extremely unfriendly to non-coders and newcomers, 
 also unmaintanable from the longer perspective
2. No roles management (e.g. moderators/editors)

# Development
I assume you have a modern Python installed. This is tested on 
version 3.6, but anything 3.2+ _should_ work, 
although not tested at all - you have to change `pyvenv-3.6` command below to
whatever version of virtualenv you have/use. So e.g. if you have `virtualenv` 
installed, just use `virtualenv .venv` instead of `pyvenv-3.6 .venv`.

```
git clone git@github.com:hnykda/eacr-wagtail.git
cd eacr-wagtail
pyvenv-3.6 .venv 
source .venv/bin/activate
pip install -r requirements.txt
cd eacr
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser # whatever you want, but remember it
python manage.py runserver
```

Now you should be up and running on `127.0.0.1:8000`. You can sign in to admin interface on `127.0.0.1:8000/admin`
with username (not email) and password you have created above (`createsuperuser` part).

# Deploy
TBD
**CREATE AND SEPARATE NEW SECRET KEY, REMOVE DB (to dangerous - contains users and passwds)**

# TODO
1. Use our styleguides within new Bootstrap
