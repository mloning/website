#!/bin/bash
# Simple alternative to Makefile, inspired by https://death.andgravity.com/run-sh
#
# usage: ./run.sh <command> [<argument> ...]
set -euo pipefail
IFS=$'\n\t'

# Run server for local development
server () { 
  port="1313"

  # open browser in background, sleep to wait for Hugo server to start
  directory="${PWD##*/}"
  url="http://localhost:$port/$directory/"
  ( sleep 1 && open "$url" ) & 

  # start Hugo server with hot reloading
  hugo server \
    --logLevel "info" \
    --port "$port" \
    --buildDrafts \
    --buildFuture \
    --navigateToChanged
}

# Add new post
new () {
  name="${1-}"
  if [ -z "$name" ]; then
    echo "Please provide the name of the new post."
    exit 1
  fi
  hugo new posts/"$name".md 
}

"$@"
