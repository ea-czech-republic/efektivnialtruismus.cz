# effectivethesis.com

This is a repository for page of effectivethesis.com

# Development
Use `docker-compose`:

```
docker-compose -f docker-compose.yaml -f dc-dev.yaml up
```

a new user `admin` with password `pass` is created. Go to
`localhost:8000/admin` to access the administration.

# Deployment
## CI
There are builds by [CircleCI](https://circleci.com/gh/ea-czech-republic/efektivnialtruismus.cz) 
and Docker images are store [Docker hub](https://cloud.docker.com/u/czea/repository/docker/czea/effective-thesis/builds).

Everything merged to `master` is deployed to production, while everything merged
to `beta` branch is deployed to `beta`.  

## How it works/manual
Through `docker-compose`. `static` and `media` files are inside 
the container, same for the `db`.

The deployment is mostly done in the `deploy.sh` script executed on
the remote machine. Everything is deployed using `docker-compose`. 

Fill in a correct IMAGE_TAG. That is a short hash of the commit (that's
how images are tagged).

```
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west3-c" "eacr-main-2" \
    --command "env IMAGE_TAG=FILL-IN-HERE ENVIRONMENT=beta|master sh /var/server/efektivnialtruismus.cz/bin/deploy.sh"
```

### Copy DB from production to Beta
```
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west3-c" "eacr-main-2" \
    --command 'docker cp efektivnialtruismuscz_app_1:"/usr/src/app/data/production-et.sqlite3" /tmp/production-eacr.sqlite3'
gcloud compute --project "efektivni-altruismus" scp --zone "europe-west3-c" "eacr-main-2:/tmp/production-eacr.sqlite3" "/tmp/production-eacr.sqlite3"
gcloud compute --project "efektivni-altruismus" scp --zone "europe-west3-c" "/tmp/production-eacr.sqlite3" "eacr-main-3:/tmp/production-eacr.sqlite3"
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west3-c" "eacr-main-3" \
    --command 'docker cp /tmp/production-eacr.sqlite3 efektivnialtruismuscz_app_1:"/usr/src/app/data/beta-et.sqlite3"'
```

### Copy media from production to Beta
```
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west3-c" "eacr-main-2" \
    --command 'docker cp efektivnialtruismuscz_app_1:"/usr/src/app/media" /tmp/media'
gcloud compute --project "efektivni-altruismus" scp --recurse --zone "europe-west3-c" "eacr-main-2:/tmp/media" "/tmp/media"
gcloud compute --project "efektivni-altruismus" scp --recurse --zone "europe-west3-c" "/tmp/media" "eacr-main-3:/tmp/media"
gcloud compute --project "efektivni-altruismus" ssh --zone "europe-west3-c" "eacr-main-3" \
    --command 'docker cp /tmp/media/. efektivnialtruismuscz_app_1:"/usr/src/app/media/"'
```

