#! /usr/bin/bash
set -e

NOW_DATE=`date +"%m_%d_%Y"`
FILENAME="website-data-"$NOW_DATE".tar.bz2"

cd /var/www/efektivnialtruismus.cz
tar -cjSf $FILENAME bin/ website/ /etc/nginx/sites-available/beta-efektivni-altruismus /etc/nginx/sites-available/production-efektivni-altruismus /etc/systemd/system/ea-cz-gunicorn@.service
$HOME/.bin/gdrive -c $HOME/.gdrive --service-account eacr-gdrive-creds.json upload -p 0BwgpG_Gt2nWnTG4zQ1NlYnI2VTA $FILENAME

rm -rf $FILENAME


# I had to create new project in google console, enable API for google drive and export credentials in JSON
# then put these in ~/.config, build gdrive by `go get github.com/prasmussen/gdrive` and then use as is above

# one more step was to create directory

# To list backups 
# gdrive --service-account eacr-gdrive-creds.json list --query " '0BwgpG_Gt2nWnTG4zQ1NlYnI2VTA' in parents"
