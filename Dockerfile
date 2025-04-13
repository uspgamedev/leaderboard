FROM python:3
 
RUN mkdir leaderboard
COPY leaderboard.py /leaderboard/.
COPY run.sh /leaderboard/.
COPY requirements.txt leaderboard/requirements.txt
WORKDIR leaderboard

RUN apt update -y
RUN apt install -y nano httpie

RUN pip install --no-cache-dir -r requirements.txt


