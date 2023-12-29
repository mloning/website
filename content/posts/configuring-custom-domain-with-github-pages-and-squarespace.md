---
title: "Configuring a custom domain with Github Pages and Squarespace"
date: 2023-12-28T11:52:52+01:00
last_modified: .Lastmod
draft: false
---

To show my website on my custom domain, I had to configure GitHub Pages, my static site hosting service, and Squarespace, my domain hosting service.

Luckily, the GitHub Pages and Squarespace docs were easy to follow. 
This [blog post] was also helpful. 

[blog post]: https://emilymdubois.medium.com/using-a-squarespace-domain-with-github-pages-438951d4f5b7

## 1. Configure custom domain for GitHub Pages 

Follow the Github Pages docs for [configuring a custom domain].

[configuring a custom domain]: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site

## 2. Configure Squarespace DNS settings for GitHub Pages 

To point our Squarespace domain to our GitHub Pages site, make these changes to the Squarespace DNS settings:

* Add a CNAME record with host "www" and `<user>.github.io`, for example, in my case `mloning.github.com`.
* Add an A record with host "@" for each GitHub Pages IP address. Use the `dig <user>.github.io` command to get this list. At the time of writing, the IP addresses are: 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153.

For more details, see the Squarespace docs on [pointing to a non-Squarespace site]. 

It can take up to [72 hours] for your new configuration to take effect.
While you wait, you can check your domain’s progress across the internet by using [whatsmydns.net].

Once your changes have propagated, you should be able to navigate to your custom domain and see your `<user>.github.io content`.
You can also check that the DNS check on the GitHub Pages page of your repository settings is successful.

[pointing to a non-Squarespace site]: https://support.squarespace.com/hc/en-us/articles/215744668#toc-point-to-a-non-squarespace-site
[72 hours]: https://support.squarespace.com/hc/en-us/articles/206206678
[whatsmydns.net]: https://www.whatsmydns.net/

## 3. Verify custom domain for GitHub Pages 

To secure your custom domain from takeovers, you need to add a TXT record.

To generate the TXT hostname and value, follow the GitHub Pages docs for [verifying a custom domain].

Then add the TXT record to the Squarespace DNS settings.
For details, see the Squarespace docs on [adding a TXT record].

Again, it can take up to 72 hours for the new DNS configuration to take effect.
Once the changes have been propagated, you can complete the domain verification on GitHub.

[adding a TXT record]: https://support.squarespace.com/hc/en-us/articles/360002101888#toc-txt-records
[verifying a custom domain]: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/verifying-your-custom-domain-for-github-pages


