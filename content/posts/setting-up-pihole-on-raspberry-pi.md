---
title: "Setting Up Pihole on Raspberry Pi"
date: 2024-04-27T*:59:05+02:00
last_modified: .Lastmod
draft: false
---

[Pi-hole]: https://pi-hole.net/
[Raspberry Pi]: https://www.raspberrypi.com/
[tutorial]: https://www.raspberrypi.com/tutorials/running-pi-hole-on-a-raspberry-pi/

I've finally had some time to set up [Pi-hole] on my [Raspberry Pi].
For most parts, I followed the excellent [tutorial] on the Raspberry Pi website.

## Set up Raspberry Pi

* On your usual computer, install an operating system onto the microSD card. For the installer, I used the [Raspberry Pi Imager](https://www.raspberrypi.com/documentation/computers/getting-started.html#install-an-operating-system). For the OS, I picked the Debian-based Raspberry Pi OS Lite (64 bit) which comes without the desktop environment. 
* Insert the microSD card into the Raspberry Pi, connect its power cable, and wait for it to boot up (green LED light).
* Connect using ssh using the user account configured in step 1: `ssh <user>@<host>.local`, for example: `mloning@anon.local` ("ânon" meaning little donkey in French).
* On the Raspberry Pi, upgrade the system packages and restart: `sudo apt-get update && sudo apt-get upgrade --yes && sudo reboot`.

A few useful commands:

* `sudo shutdown -h now` to shut down. To start it again, re-connect the power cable
* `sudo reboot` to restart
* `htop` for monitoring processes and resource usage

## Easier login with ssh key

Optionally, for an easier login experience, you can use an ssh key:

On your usual computer:

* Start the ssh-agent in the background: `eval "$(ssh-agent -s)"`.
* Generate ssh key: `ssh-keygen -f ~/.ssh/<key-name> -C <user>`, for example: `ssh-keygen -f ~/.ssh/id_raspberrypi -C <user>`.
* Copy the public key to Raspberry Pi: `ssh-copy-id -i ~/.ssh/<key-name>.pub <user>@<host>.local`, for example: `ssh-copy-id -i ~/.ssh/id_raspberrypi.pub mloning@anon.local`.
* Configure ssh settings in `~/.ssh/config`, for example:

```
Host anon
  HostName anon.local
  User mloning
  IdentityFile ~/.ssh/id_raspberrypi
  UseKeyChain yes
  AddKeysToAgent yes
```

These settings are for MacOS; they may be different for other operating systems.

To connect to your Raspberry Pi from your usual computer, you should now be able to simply run: `ssh anon`.

## Assigning a static IP address to the Raspberry Pi

From the Raspberry Pi:

* `nmcli device status`, or specifically: `nmcli device show eth0` for the `eth0` interface, to see if [Network Manager](https://developer-old.gnome.org/NetworkManager/stable/nmcli.html) manages the device
* `nmcli connection show` to get the current connection name
* `sudo nmcli connection modify <name> ...` to modify the connection, for example: `sudo nmcli connection modify "Wired connection 1" ipv4.method "manual" ipv4.addresses "192.168.1.19/24" ipv4.gateway "192.168.1.1"`
* `sudo systemctl restart NetworkManager` to restart the Network Manager

Alternatively, you can use the terminal UI `mntui` (see this [blog post](https://www.jeffgeerling.com/blog/2024/set-static-ip-address-nmtui-on-raspberry-pi-os-12-bookworm) for details).

Log in to your router's admin page. If you don't know the address, you can find it using: `nmcli -f IP4.GATEWAY device show wlan0`, assuming your usual computer is connected via `wlan0` and not `eth0`.

From your router's admin page:

* Assign the same static IP to the Raspberry Pi. 

## Install Pi-hole

On the Raspberry Pi:

* To install Pi-hole, run: `curl -sSL https://install.pi-hole.net | bash`. In the [tutorial], the Raspberry Pi is connected via WiFi, with the `wlan0` interface being configured in the installation. If you can connect via an Ethernet cable, that's usually the preferred choice as it's more reliable, using `eth0` for the interface.
* Make a note of the IP address and admin password for the dashboard (or store it in your password manager). 

To check if Pi-hole is running, try:

* `pihole status`
* `pihole -c` to open the console dashboard,
* opening `http://<host>/admin/` (for example, `http://anon.local/admin/`) in the browser of your usual computer to login to the admin dashboard using the admin password.

If you want to reconfigure Pi-hole later, run: `pihole -r` and select "reconfigure".

## Configure Pi-hole as your network's DHCP provider

My router did not allow me to set a DNS server, so I configured the DHCP provider instead.
For other options, see the [tutorial].

* Disable your router's default DHCP provider.

From the Pi-hole admin dashboard:

* Enable Pi-hole as the DHCP provider in "settings" under "DHCP".

## Check if Pi-hole is working

* https://adblock-tester.com/



