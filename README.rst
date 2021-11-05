Suorafxctl - Configure Roccat Suora FX keyboards on Linux
=========================================================

Suorafxctl is a small CLI tool and Python library to configure Roccat Suora FX gaming keyboards on Linux. Only supports most simple settings, such as predefined lighting effects, brightness, effect speed and basic effect colors, are supported.


Usage
-----

::

    usage: suorafxctl [-h] [-e EFFECT] [-s 0-10] [-b 0-50] [-c COLOR] [-r]

    optional arguments:
      -h, --help            show this help message and exit
      -e EFFECT, --effect EFFECT
                            Illumination effect (full-lit, breathing, color-shift, wave-right,
                            wave-left, wave-up, wave-down, fade-out, fade-in, ripple, rain,
                            snake, spiral, game-over, scanner, radar)
      -s 0-10, --speed 0-10
                            Illumination effect speed, from 0 (fast) to 10 (slow)
      -b 0-50, --brightness 0-50
                            keyboard brightness, from 0 (light off) to 50
      -c COLOR, --color COLOR
                            Illumination color (red, green, yellow, blue, aqua, purple, white)
      -r, --reset           reset all settings to their default

    The first call to this command will reset all unspecified settings to their default value


Installing suorafxctl from sources
----------------------------------

You will first need to install libusb1 and Git. On Ubuntu / Debian you can achieve this with the following command::

    sudo apt install python3-libusb1 git

Then clone this repository and go to the project's folder::

    git clone https://github.com/flozz/suorafxctl.git
    cd suorafxctl

Then install the project::

    sudo pip install .

You can now run the software as root::

    sudo suorafxctl --help


Installing udev rules
---------------------

For being able to run ``suorafxctl`` as a standard user, you must configure udev. To do so, just copy the ``99-roccat-suora-fx.rules`` file of this repository to ``/etc/udev/rules.d/``::

    sudo cp ./99-roccat-suora-fx.rules /etc/udev/rules.d/

Then update udev rules::

    sudo udevadm trigger

And finally unplug / replug the keyboard to the computer.


Changelog
---------

TODO
