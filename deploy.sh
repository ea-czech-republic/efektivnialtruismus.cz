#!/bin/bash

bundle exec jekyll build

if [ "$USER" == prvak ]; then
	s3cmd -c ~/dropbox/hesla/ea-cr/s3cfg-efektivnialtruismus.cz sync --delete-removed --recursive _site/* s3://efektivni-altruismus.cz/
else
	s3cmd sync --delete-removed --recursive _site/* s3://efektivni-altruismus.cz/
fi

