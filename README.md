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

```
gcloud compute \
    --project "efektivni-altruismus" \
    ssh \ 
    --zone "europe-west1-c" \
    "eacr-main" \
    --command "env IMAGE_TAG=FILL_IN_HERE sh /var/server/efektivnialtruismus.cz/bin/deploy.sh"
```


# Migration
To dump and upload the db:
```
scp freevps:/home/comus/www/dan/efektivnialtruismus/deploy/production/files/website/production-eacr.sqlite3 .
gcloud compute --project "efektivni-altruismus" scp --zone "europe-west1-c" production-eacr.sqlite3 eacr-main:~
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west1-c" "eacr-main" \
    --command 'docker cp production-eacr.sqlite3 efektivnialtruismuscz_app_1:"/usr/src/app/data/beta-eacr.sqlite3"'
```

Media:
```
scp -r freevps:/home/comus/www/dan/efektivnialtruismus/deploy/production/files/website/media media-bckp
gcloud compute --project "efektivni-altruismus" scp --zone "europe-west1-c" media-bckp eacr-main:~/media-bckp
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west1-c" "eacr-main" \
    --command 'docker cp media-bckp/* efektivnialtruismuscz_app_1:"/usr/src/app/media"'
```