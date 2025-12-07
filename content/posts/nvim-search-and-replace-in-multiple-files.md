---
title: Search and replace in multiple files using vim
date: 2024-12-24T09:35:15+01:00
draft: false
---
I'm using Neovim with [AstroNvim], and the key maps below will be different depending on your setup.
You can find my configuration [here](https://github.com/mloning/dotfiles).

To find and replace a string in multiple files, you can use this workflow:

- Use [telescope] to find occurrences of the string (`<leader>fw`)
- Send the results to the [quickfix list] (`C-q`)
- Use the `cfdo` command to replace the string for all occurrences in the quickfix list: `cfdo %s/<old-string>/<new-string>/g | write`

To open the quickfix list, type: `<leader>xq`, or using [Trouble]: `<leader>xQ`.

Also check out these blog posts:

- https://benfrain.com/neovim-how-to-do-project-wide-find-and-replace/
- https://thevaluable.dev/vim-search-find-replace/

[AstroNvim]: https://astronvim.com/
[quickfix list]: https://neovim.io/doc/user/quickfix.html
[Trouble]: https://github.com/folke/trouble.nvim
[telescope]: https://github.com/nvim-telescope/telescope.nvim
