#!/bin/bash

yum install docker git ffmpeg -y
service docker start
git clone https://github.com/homelabwithkevin/playground.git
cd playground/yt-dlp/code
git checkout yt-dlp/docker-simple
docker build . -t app

# cd /tmp && wget https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz && tar xf ffmpeg-release-arm64-static.tar.xz && cd ffmpeg-7* && cp ffmpeg /usr/bin/ffmpeg && cp ffprobe /usr/bin/ffprobe

ffmpeg \
        -i {example}.mp4 \
        -c:v libx264 \
        -c:a copy \
        -flags +cgop \
        -g 30 \
        -hls_time 10 \
        -hls_playlist_type event \
        {example}.m3u8


https://dypk3q4dgs56m.cloudfront.net/{example}/{example}.mp4