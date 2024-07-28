FROM python:3-alpine

# Update installed packages and install Apache
RUN pip install yt-dlp boto3

COPY . .

CMD [ "python", "./container.py" ]

# RUN echo 'yt-dlp https://www.youtube.com/watch?v=4sW0isKaPAE' >> /root/run_apache.sh && 
#  chmod 755 /root/run_apache.sh

# CMD /root/run_apache.sh

# docker tag hello-world 654654599343.dkr.ecr.us-east-1.amazonaws.com/hlb-yt-dlp:latest