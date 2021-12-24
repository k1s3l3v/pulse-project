#!/usr/bin/env bash

yarn install
yarn build

docker build -t prj_ui .
docker run -d --name prj_ui -p 3003:80 --restart always prj_ui

sudo rsync -avP nginx/prj.conf /etc/nginx/conf.d/
sudo nginx -t && sudo nginx -s reload
sudo certbot --nginx -d prj.pmsociety.su
