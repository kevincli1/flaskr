#!/bin/sh
# this script is used to boot a Docker container
sleep 15
if [[ "$DATABASE_MIGRATE" == '1' ]]; then
    while true; do
        flask db upgrade
        if [[ "$?" == "0" ]]; then
            break
        fi
        echo Deploy command failed, retrying in 5 secs...
        sleep 5
    done
fi 
exec gunicorn -k gevent -b :5000 --access-logfile - --error-logfile - --worker-tmp-dir /dev/shm 'flaskr:create_app()'
