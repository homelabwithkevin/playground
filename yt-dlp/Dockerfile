FROM python:3.10-alpine

COPY requirements.txt requirements.txt
RUN pip install Flask yt-dlp

COPY code .
RUN ls
CMD [ "python", "-m" , "flask", "--app", "main", "run", "--host=0.0.0.0"]