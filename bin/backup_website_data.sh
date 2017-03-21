#! /usr/bin/bash
set -e

NOW_DATE=`date +"%m_%d_%Y"`
FILENAME="website-data-"$NOW_DATE".tar.bz2"

cd /var/www/efektivnialtruismus.cz
tar -cjSf $FILENAME bin/ website/ /etc/nginx/sites-available/beta-efektivni-altruismus /etc/nginx/sites-available/production-efektivni-altruismus /etc/systemd/system/ea-cz-gunicorn@.service
$HOME/.bin/gdrive -c $HOME/.gdrive --service-account eacr-gdrive-creds.json upload -p 0BwgpG_Gt2nWnTG4zQ1NlYnI2VTA $FILENAME

rm -rf $FILENAME
