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