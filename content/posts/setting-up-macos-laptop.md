---
title: "Setting up a new macOS laptop"
date: 2024-09-27T13:49:57+02:00
last_modified: .Lastmod
draft: false
---

I recently had to set up a new macOS laptop and wanted to take some notes so that I can do it more quickly the next time.
This [blog post](https://simoncw.com/posts/dev-setup-mac-python-rust/) was very useful.

## Manual configuration

Some things I configure manually, even though they could be automated:

- Add Bluetooth icon in control center bar
- Add sound icon in control center bar
- Set trackpad "click on tap"
- `defaults write -g ApplePressAndHoldEnabled -bool false`

## Install command-line tools

```bash
xcode-select --install
```

## Install homebrew

Install homebrew:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Add `brew` command to path:

```bash
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/mloning/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

## Install system packages

```bash
brew install \
  neovim \
  tmux \
  alacritty \
  eza \
  stow \
  bat \
  fzf \
  fd \
  gh \
  gpg \
  node \
  htop \
  tree \
  ripgrep \
  bitwarden \
  llvm \
  jq
```

## Install oh-my-zsh with powerlevel10k

Install [oh-my-zsh] with plugins specified in `.zshrc` file:

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/zsh-users/zsh-autosuggestions.git $ZSH_CUSTOM//plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git $ZSH_CUSTOM/plugins/zsh-syntax-highlighting
git clone https://github.com/TamCore/autoupdate-oh-my-zsh-plugins $ZSH_CUSTOM/plugins/autoupdate
omz reload
```

In addition, I install the [powerlevel10k] theme:

- Install fonts: https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#manual-font-installation
- Install powerlevel10k: https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#oh-my-zsh

[oh-my-zsh]: https://ohmyz.sh/
[powerlevel10k]: https://github.com/romkatv/powerlevel10k

## Install my dotfiles

Next, I add my configuration files from my [dotfiles repo](https://github.com/mloning/dotfiles):

```bash
mv ~/.zshrc ~/.zshrc.bak
mkdir ~/Dev/projects
cd ~/Dev/projects
git clone https://github.com/mloning/dotfiles.git
cd dotfiles
make create
omz reload
```

## Install tmux plugins

```bash
git clone https://github.com/tmux-plugins/tpm ~/.tmux/plugins/tpm
```

To install the plugins, open a tmux session and press: tmux prefix (`C-a`) + `I`.

## Install Python

Install [miniforge]:

```bash
brew install miniforge
conda init "$(basename "${SHELL}")"
omz reload
conda info
```

[miniforge]: https://github.com/conda-forge/miniforge

## Create GPG keys

Finally, if you want to [sign your git commits](https://withblue.ink/2020/05/17/how-and-why-to-sign-git-commits.html) using GPG keys, you have to generate new keys and add them to your GitHub account.
