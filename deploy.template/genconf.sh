#!/bin/sh

cd ..

if [[ -d 'deploy/' ]]; then
    echo "Error: Directory 'deploy/' is exists."
    exit 1
fi

cp -r deploy.template deploy
cd deploy/
rm -rf genconf.sh
mv template.nginx nginx.conf
mv template.supervisor.conf supervisor.conf
mv template.uwsgi.ini uwsgi.ini

exit 0
