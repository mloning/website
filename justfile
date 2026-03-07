default:
    just --list

# Run dev server for local development
run-dev-server:
    (sleep 1 && open "http://localhost:1313/website/") &
    hugo server \
        --logLevel "info" \
        --port "1313" \
        --buildDrafts \
        --buildFuture \
        --navigateToChanged

# Add new post
create-new-post name:
    hugo new posts/{{name}}.md

alias s := run-dev-server
alias n := create-new-post

