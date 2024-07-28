#!/bin/bash

yum install docker git ffmpeg -y
service docker start
git clone https://github.com/homelabwithkevin/playground.git
cd playground/yt-dlp/code
git checkout yt-dlp/docker-simple
docker build . -t app
