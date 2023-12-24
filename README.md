# My website

My personal website built with [Hugo] and a modified [ezhil] theme.

[Hugo]: https://gohugo.io
[ezhil]: https://github.com/mloning/ezhil

## Local development

* `git submodule update --init --recursive` to update the theme as a [git submodule]
* `hugo server --verbose --buildDrafts --buildFuture --navigateToChanged` to start the Hugo server with hot reloading
* `hugo new posts/<name>.md` to create a new draft in `content/posts/`

[git submodule]: https://git-scm.com/book/en/v2/Git-Tools-Submodules

## Deploy 

Deployed to GitHub Pages using GitHub Actions.


