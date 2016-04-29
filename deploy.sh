#!/bin/bash

bundle exec jekyll build
s3cmd sync --recursive _site/* s3://efektivni-altruismus.cz/

