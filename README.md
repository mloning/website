# My website

My personal website built with [Hugo] and a modified [Ezhil] theme.

[Hugo]: https://gohugo.io
[Ezhil]: https://github.com/mloning/ezhil

## Local development

* `gh repo clone https://github.com/mloning/website . -- --recurse-submodules` to clone the repo with the theme as a [git submodule]
* `git submodule update --init --recursive --remote` to update the theme from the git submodule
* `./run.sh server` to start the Hugo server with hot reloading
* `./run.sh new <name>` to create a new draft in `./content/posts/<name>.md`

[git submodule]: https://git-scm.com/book/en/v2/Git-Tools-Submodules

## Deploy 

Pushing changes to the `main` branch will trigger a deployment using a [GitHub Action] and [GitHub Pages].

[GitHub Pages]: https://mloning.github.io/website/
[GitHub Action]: https://github.com/mloning/website/actions/workflows/deploy.yaml 

## Configure a custom domain

Check out the GitHub Pages docs for [configuring a custom domain] and this [blog post]. 

[configuring a custom domain]: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
[blog post]: https://emilymdubois.medium.com/using-a-squarespace-domain-with-github-pages-438951d4f5b7
