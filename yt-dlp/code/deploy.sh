aws ecr get-login-password --region us-east-1 | sudo docker login --username AWS --password-stdin 654654599343.dkr.ecr.us-east-1.amazonaws.com
sudo docker build -t hlb-yt-dlp .
sudo docker tag hlb-yt-dlp:latest 654654599343.dkr.ecr.us-east-1.amazonaws.com/hlb-yt-dlp:latest
sudo docker push 654654599343.dkr.ecr.us-east-1.amazonaws.com/hlb-yt-dlp:latest
