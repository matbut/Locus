#!/bin/bash -e

function cleanup {
  echo -e "\n\e[33mExit\e[39m"
  kill -9 $WORKERS
}

echo -e "\e[33mStarting workers\e[39m"
nohup python3 manage.py runworker db_ftsearcher db_url_searcher twitter_url_searcher twitter_text_searcher google_searcher internet_search_manager & > workers.log
WORKERS=$!
echo "Workers are running in background. Process ID: $WORKERS"

echo -e "\e[33mStarting web server\e[39m"
python3 manage.py runserver

trap cleanup EXIT
