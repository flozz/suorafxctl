Suorafxctl - Configure Roccat Suora FX keyboards on Linux
=========================================================

|Github| |Discord| |PYPI Version| |Github Actions| |Black| |License|

Suorafxctl is a small CLI tool and Python library to configure Roccat Suora FX gaming keyboards on Linux. Only most simple settings, such as predefined lighting effects, brightness, effect speed and basic effect colors, are supported.


Usage (CLI)
-----------

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


Usage (Python Library)
----------------------

.. code-block:: Python

    from suorafxctl import SuoraFX

    suorafx = SuoraFX()

    # Get control of the USB device
    suorafx.acquire()

    # Set some configs
    suorafx.effect = "wave-right"
    suorafx.speed = 1
    suorafx.brightness = 50
    suorafx.color = "red"

    # Send configs to the device
    suorafx.commit()

    # Return the control of the USB device to the Linux Kernel
    suorafx.release()


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

* **[NEXT]** (changes on ``master``, but not released yet):

  * Nothing yet :)

* **v1.0.1:**

  * chore: Added Python 3.11 and 3.12 support
  * chore!: Removed Python 3.7 support

* **v1.0.0:** Initial release

.. |Github| image:: https://img.shields.io/github/stars/flozz/suorafxctl?label=Github&logo=github
   :target: https://github.com/flozz/suorafxctl

.. |Discord| image:: https://img.shields.io/badge/chat-Discord-8c9eff?logo=discord&logoColor=ffffff
   :target: https://discord.gg/P77sWhuSs4

.. |PYPI Version| image:: https://img.shields.io/pypi/v/suorafxctl?logo=python&logoColor=f1f1f1
   :target: https://pypi.org/project/suorafxctl/

.. |Github Actions| image:: https://github.com/flozz/suorafxctl/actions/workflows/python-ci.yml/badge.svg
   :target: https://github.com/flozz/suorafxctl/actions

.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://black.readthedocs.io/en/stable/

.. |License| image:: https://img.shields.io/github/license/flozz/suorafxctl
   :target: https://github.com/flozz/suorafxctl/blob/master/LICENSE
