# My website

My personal website built with [Hugo] and a modified [Ezhil] theme.

[Hugo]: https://gohugo.io
[Ezhil]: https://github.com/mloning/ezhil

## Local development

- `gh repo clone https://github.com/mloning/website . -- --recurse-submodules` to clone the repo with the theme as a [git submodule]
- `git submodule update --init --recursive --remote` to update the theme from the git submodule
- `./run.sh server` to start the Hugo server with hot reloading
- `./run.sh new <name>` to create a new draft in `./content/posts/<name>.md`
- Use `Cmd` + `Shift` + `R` to force reload the cache in Firefox

[git submodule]: https://git-scm.com/book/en/v2/Git-Tools-Submodules

## Deploy

Pushing changes to the `main` branch will trigger a deployment using a GitHub Action [workflow] and GitHub Pages.

[workflow]: https://github.com/mloning/website/actions/workflows/deploy.yaml

## Configure custom domain

Check out my blog post on [how to configure a custom domain with GitHub Pages and Squarespace].

[how to configure a custom domain with GitHub Pages and Squarespace]: https://www.mloning.com/posts/configuring-custom-domain-with-github-pages-and-squarespace/
