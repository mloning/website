---
title: "Setting Up Pihole on Raspberry Pi"
date: 2024-04-27T14:59:05+02:00
last_modified: .Lastmod
draft: true
---

[Pi-hole]: https://pi-hole.net/
[Raspberry Pi]: https://www.raspberrypi.com/
[tutorial]: https://www.raspberrypi.com/tutorials/running-pi-hole-on-a-raspberry-pi/

I've finally had some time to set up [Pi-hole] on my [Raspberry Pi].

For most parts, I followed the excellent [tutorial] on the Raspberry Pi website.

## Initial setup 


1. On your usual computer, install an operating system on the microSD card. I used the [Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system). Make sure to configure the user account (username, password), WiFi settings, and host name.
1. Insert microSD card into the Raspberry Pi. 
1. Wait for the Raspberry Pi to boot.
1. Connect using ssh using the user account configured in step 1: `ssh <user>@<host>.local`, for example: `mloning@raspberrypi.local`.
1. On the Raspberry Pi, upgrade the system packages and restart: `sudo apt-get update && sudo apt-get upgrade --yes && sudo reboot`.

## Easier login with ssh key

Optionally, for an easier login experience, you can use an ssh key:

On your usual computer:

1. Start the ssh-agent in the background: `eval "$(ssh-agent -s)"`.
1. Generate ssh key: `ssh-keygen -f ~/.ssh/<key-name> -C <user>`, for example: `ssh-keygen -f ~/.ssh/id_raspberrypi -C <user>`.
1. Copy the public key to Raspberry Pi: `ssh-copy-id -i ~/.ssh/<key-name>.pub <user>@<host>.local`, for example: `ssh-copy-id -i ~/.ssh/id_raspberrypi.pub mloning@raspberrypi.local`.
1. Configure ssh settings in `~/.ssh/config`, for example:

```
Host pi
  HostName raspberrypi.local
  User mloning
  IdentityFile ~/.ssh/id_raspberrypi
  UseKeyChain yes
  AddKeysToAgent yes
```

These settings are for MacOS; they may be different for other operating systems.

To connect to your Raspberry Pi from your usual computer, you should now be able to simply run: `ssh pi`.

## Install Pi-hole

On the Raspberry Pi:

1. Install Pi-hole: `curl -sSL https://install.pi-hole.net | bash`. Make a note of the IP address and admin password for the dashboard (or store it in your password manager). 

To check if Pi-hole is running, try:

* `pihole status`
* `pihole -c` to open the console dashboard,
* opening `http://<host>/admin/` (for example, `http://raspberrypi.local/admin/`) in the browser of your usual computer to login to the admin dashboard using the admin password.

## Configure Pi-hole as your network's DNS server

My router did not allow me to set a DNS server, so I configured the DHCP provider instead.
For other options, see the [tutorial].

1. Log in to your router's admin page. If you don't know the address, you can find it using: `nmcli -f IP4.GATEWAY device show wlan0` 

## Check if Pi-hole is working

1. https://adblock-tester.com/


