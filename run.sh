#!/bin/bash
# Simple alternative to Makefile, inspired by https://death.andgravity.com/run-sh
#
# usage: ./run.sh <command> [<argument> ...]

set -euo pipefail
IFS=$'\n\t'

# Run server for local development
server () { 
	hugo server --verbose --buildDrafts --buildFuture --navigateToChanged
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
