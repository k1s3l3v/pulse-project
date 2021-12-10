#!/usr/bin/env bash

yarn install
yarn build

docker build -t prj_ui .
docker rm -f prj_ui || true
docker run -d --name prj_ui -p 3003:80 --restart always prj_ui
