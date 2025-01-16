---
title: "Signing git commits"
date: 2025-01-14T20:50:10+01:00
last_modified: .Lastmod
draft: true
---

https://withblue.ink/2020/05/17/how-and-why-to-sign-git-commits.html

If a key expires, you can update the expiration date as follows:

- `gpg --list-secret-keys` to list the secret keys and look up the key ID, alternatively `gpg --list-keys`
- `gpg --edit-key <key-id>` to open the gpg console
- run `expire` in the gpg console and follow the prompts to update the expiration date
- finally `save` and `quit`

You can type `help` in the console for other available commands.
