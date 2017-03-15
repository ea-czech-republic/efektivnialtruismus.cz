# efektivnialtruismus.cz on Wagtail

This page is for efektivni-altruismus.cz. It is based on Python `wagtail` CMS. 
It is also rewritten from scratch using Bootstrap 4.

# How to get this
```
TBD
```

# Development
I assume you have a modern Python installed. This is tested on 
version 3.6, but anything 3.2+ _should_ work, 
although not tested at all. 

## How to set up the dev environment

Run `bash bin/init-run.sh` from the root dir of this repo.

Now you should be up and running on `127.0.0.1:8000`. You can sign in to admin interface on `127.0.0.1:8000/admin`
with username (not email) and password you have created above (`createsuperuser` part).

# Deploy
Create separate `bin/production-env.sh` where you specify variables such as:
```
#!/usr/bin/env bash
export SENDGRID_API_KEY="xxx"
export DEBUG=False
export ALLOWED_HOSTS="www.efektivni-altruismus.cz efektivni-altruismus.cz"
export SECRET_KEY="xxx"
export EMAIL_BACKEND="sgbackend.SendGridBackend"
```

then `source bin/production-env.sh` and run server (probably using something like `gunicorn+nginx`).

You also need to run `python manage.py collectstatic` to collect static files for `nginx`.


# The choice
The choice of the frameworks `bootstrap` and `wagtail` is based on ease of use,
since there will be probably often a change in who manage the site. Both
have strong community and documentation. 

# Why to move?
1. current solution is extremely unfriendly to non-coders and newcomers, 
 also unmaintanable from the longer perspective
2. No roles management (e.g. moderators/editors)

# Tips

## Sourcing all vars from the file

`export $(cut -d= -f1 bin/beta-env.sh)`

## example systemd unit to run gunicorn
```
[Unit]
ConditionFileNotEmpty=/var/www/efektivnialtruismus.cz/bin/%i-env.sh
Description=Gunicorn daemon for efektivni-altruismus.cz on wagtail (django) with settings %I

[Service]
Type=simple
User=webdata
Group=webdata
WorkingDirectory=/var/www/efektivnialtruismus.cz
EnvironmentFile=/var/www/efektivnialtruismus.cz/bin/%i-env.sh
ExecStart=/usr/bin/bash bin/gunicorn-start.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```
save it as `/etc/systemd/system/ea-cz-gunicorn@.service` and then run it by

```
systemctl start ea-cz-gunicorn@<ENVIRONMENT-FILE-IN-BIN>.service
```
