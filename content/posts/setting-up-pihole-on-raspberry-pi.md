---
title: "Setting up Pi-hole on Raspberry Pi"
date: 2024-04-27T23:59:05+02:00
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

## Easier login with ssh key and configuration

For an easier login experience, you can use an ssh key. 
This allows you to login without having to type your password every time.
From your usual computer:

* Start the ssh-agent in the background: `eval "$(ssh-agent -s)"`.
* Generate the pair of private and public ssh keys: `ssh-keygen -f ~/.ssh/<key-name> -C <user>`, for example: `ssh-keygen -f ~/.ssh/id_raspberrypi -C <user>`.
* Copy the public key to the Raspberry Pi: `ssh-copy-id -i ~/.ssh/<key-name>.pub <user>@<host>.local`, for example: `ssh-copy-id -i ~/.ssh/id_raspberrypi.pub mloning@anon.local`.

You should now be able to connect without your password using: `ssh <user>@<host>.local`.

To make this even easier, you can configure ssh settings in `~/.ssh/config`. 
For example:

```
Host anon
  HostName anon.local
  User mloning
  IdentityFile ~/.ssh/id_raspberrypi
  UseKeyChain yes
  AddKeysToAgent yes
```

You should now be able to simply run: `ssh anon`.

To log out, simply run: `exit`.

## Assigning a static IP address to the Raspberry Pi

From the Raspberry Pi, run:

* `nmcli device status`, or specifically: `nmcli device show eth0` for the `eth0` interface, to verify that [Network Manager](https://developer-old.gnome.org/NetworkManager/stable/nmcli.html) manages the device
* `nmcli connection show` to get the current connection name
* `sudo nmcli connection modify <name> ...` to modify the connection, for example: `sudo nmcli connection modify "Wired connection 1" ipv4.method "manual" ipv4.addresses "192.168.1.19/24" ipv4.gateway "192.168.1.1"`
* `sudo systemctl restart NetworkManager` to restart Network Manager

Alternatively, you can use the terminal UI `mntui` (see this [blog post](https://www.jeffgeerling.com/blog/2024/set-static-ip-address-nmtui-on-raspberry-pi-os-12-bookworm) for details).

You can also set the static IP from your router's admin page:

* Assign the same static IP to the Raspberry Pi. Usually, you can look for a list of connected devices, find your Raspberry Pi’s IP address or MAC address, and then select an option to always use this IP address to make the IP address static.

If you don't know the address of your router's admin page, you can find it using: `nmcli -f IP4.GATEWAY device show wlan0`, assuming your computer is connected via `wlan0`.

## Install Pi-hole

On the Raspberry Pi:

* To install Pi-hole, run: `curl -sSL https://install.pi-hole.net | bash`. 
* Make a note of the IP address and admin password for the dashboard (or store it in your password manager). 

In the [tutorial], the Raspberry Pi is connected via WiFi, with the `wlan0` interface being configured in the installation. If you can connect via an Ethernet cable using `eth0` for the interface, that's usually the preferred choice as it's more reliable.

After the installation, check if Pi-hole is running:

* `pihole status`,
* `pihole -c` to open the console dashboard.

If you want to reconfigure Pi-hole later, you can always run: `pihole -r` and select "reconfigure".

## Configure Pi-hole as your network's DHCP provider

My router did not allow me to set a DNS server, so I configured Pi-hole as my DHCP provider instead.
For other options, see the [tutorial].

From your router's admin page:

* Disable your router's default DHCP provider.

Next, open the Pi-hole admin dashboard in your browser at: `http://<host>/admin/` (for example, `http://anon.local/admin/`) using the admin password from the Pi-hole installation step above.
From the Pi-hole admin dashboard:

* Enable Pi-hole as the DHCP provider in "settings" under "DHCP".

You may want to restart your router afterwards. On your computer, you can also try to renew your IP address from the DHCP server. Your usual computer should then show up under the "Currently active DHCP leases" on the Pi-hole admin dashboard "DHCP" settings page.

## Check if Pi-hole is working

Finally, verify that Pi-hole is working:

* Check out: https://adblock-tester.com/
* Visually check ads are being displayed on websites when on your local network

## Update Pi-hole

To update Pi-hole, run: `pihole -up`.

