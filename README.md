# My website

My personal website built with [Hugo] and a modified [Ezhil] theme.

[Hugo]: https://gohugo.io
[Ezhil]: https://github.com/mloning/ezhil

## Local development

* `gh repo clone https://github.com/mloning/website . -- --recurse-submodules` to clone the repo with the theme as a [git submodule]
* `git submodule update --init --recursive` to update the theme from the git submodule
* `hugo server --verbose --buildDrafts --buildFuture --navigateToChanged` to start the Hugo server with hot reloading
* `hugo new posts/<name>.md` to create a new draft in `content/posts/`

[git submodule]: https://git-scm.com/book/en/v2/Git-Tools-Submodules

## Deploy 

Pushing changes to the `main` branch will trigger a deployment to [GitHub Pages] using a [GitHub Action].

[GitHub Pages]: https://mloning.github.io/website/
[GitHub Action]: https://github.com/mloning/website/actions/workflows/deploy.yaml 
