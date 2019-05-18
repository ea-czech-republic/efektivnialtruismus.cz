# effectivethesis.com

This is a repository for page of effectivethesis.com

# Development
Use `docker-compose`:

```
docker-compose up
```

a new user `admin` with password `pass` is created. Go to
`localhost:8000/admin` to access the administration.

# Deployment
Through `docker-compose`. `static` and `media` files are inside 
the container, same for the `db`.

The deployment is mostly done in the `deploy.sh` script executed on
the remote machine. Everything is deployed using `docker-compose`. 

Fill in a correct IMAGE_TAG. That is a short hash of the commit (that's
how images are tagged).

```
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west3-c" "eacr-main-2" \
    --command "env IMAGE_TAG=FILL-IN-HERE sh /var/server/efektivnialtruismus.cz/bin/deploy.sh"
```

## Builds
[Google Cloud Builds](https://console.cloud.google.com/cloud-build/builds?project=efektivni-altruismus&authuser=2&supportedpurview=project)

# Migration from freevps
To dump and upload the db:
```
scp freevps:/home/comus/www/dan/efektivnialtruismus/deploy/production/files/website/production-eacr.sqlite3 .
gcloud compute --project "efektivni-altruismus" scp --zone "europe-west3-c" production-eacr.sqlite3 eacr-main-2:~
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west3-c" "eacr-main-2" \
    --command 'docker cp production-eacr.sqlite3 efektivnialtruismuscz_app_1:"/usr/src/app/data/production-et.sqlite3"'
```
after a new fresh deploy, I have to retrigger `docker exec efektivnialtruismuscz_app_1 python website/manage.py migrate`
because I copied the database *after* the migration command when the container starts.

Media:
```
scp -r freevps:/home/comus/www/dan/efektivnialtruismus/deploy/production/files/website/media media-bckp
gcloud compute --project "efektivni-altruismus" scp --recurse --zone "europe-west3-c" media-bckp eacr-main-2:~/media-bckp
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west3-c" "eacr-main-2" \
    --command 'docker cp media-bckp/. efektivnialtruismuscz_app_1:"/usr/src/app/media"'
```
