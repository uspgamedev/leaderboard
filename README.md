# UGD Leaderboard

## Usage

usage: Leaderboard [-h] [-p PORT] [-l LEADERBOARDS [LEADERBOARDS ...]]

A simple leaderboard API.

Endpoints:
 - GET /leaderboard/<leaderboard> - Top 10 scores;
 - GET /leaderboard/<leaderboard>/<size> - Top <size> scores;
 - GET /leaderboard/<leaderboard>/rank/<score> - Rank of score <score>;
 - POST /leaderboard/<leaderboard> - Sumbit name and score.
  
options:
  -h, --help            show this help message and exit
  -p, --port PORT       port to listen
  -l, --leaderboards LEADERBOARDS [LEADERBOARDS ...] list of leaderboards to create/use

## Docker
 - run `up_run.sh <leaderboards>`  
