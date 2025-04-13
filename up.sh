#!/bin/bash

docker build -t leaderboard .

docker run -it --volume ${PWD}/db:/leaderboard/db -p 8282:8282/tcp leaderboard bash
