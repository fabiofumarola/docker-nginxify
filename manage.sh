#!/usr/bin/env bash

case $1 in
  clean_conf)
    rm -f ./nginx/conf.d/*
    ;;
  gen_default)
    ./nginxify.py --default True
    ;;
  gen_all)
    ./nginxify.py --overwrite True
    ;;
  start)
    ./nginxify.py --default True
    docker-compose up -d
    ;;
  restart)
    ./nginxify.py --default True
    docker-compose restart
    ;;
  reload)
    name=`docker-compose ps -q`
    docker exec -it ${name} /usr/sbin/nginx -t
    ;;
  stop)
    docker-compose stop
    docker-compose rm -f
    ;;
  *)
    echo 'usage manage.sh [clean_conf | gen_default | gen_all | start | restart | reload | stop]'
esac
