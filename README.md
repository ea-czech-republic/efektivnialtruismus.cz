# effectivethesis.com

This is a repository for page of effectivethesis.com

# Development
Use `docker-compose`:

```
docker-compose -f docker-compose.yaml -f dc-dev.yaml up
```

a new user `admin` with password `pass` is created. Go to
`localhost/admin` to access the administration.

# Deployment
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

## Builds
https://circleci.com/gh/ea-czech-republic/efektivnialtruismus.cz

