#!/usr/bin/env python3

import os
import sys
import json
import argparse

import usb1


def get_xdg_config_home():
    """Returns the path of the folder where to store the configs (generally
    ``$HOME/.config``).

    :rtype: str
    """
    if "XDG_CONFIG_HOME" in os.environ and os.environ["XDG_CONFIG_HOME"]:
        return os.environ["XDG_CONFIG_HOME"]
    return os.path.join(os.path.expanduser("~"), ".config")


class SuoraFX(object):

    VENDOR_ID = 0x1E7D
    PRODUCT_ID = 0x3246
    INTERFACE = 0x03

    EFFECTS = {
        "full-lit": [0x01, 0x00],
        "breathing": [0x02, 0x00],
        "color-shift": [0x08, 0x00],
        "wave-right": [0x03, 0x01],
        "wave-left": [0x03, 0x02],
        "wave-up": [0x03, 0x03],
        "wave-down": [0x03, 0x04],
        "fade-out": [0x04, 0x00],
        "fade-in": [0x07, 0x00],
        "ripple": [0x06, 0x00],
        "rain": [0x0A, 0x00],
        "snake": [0x05, 0x00],
        "spiral": [0x0B, 0x00],
        "game-over": [0x09, 0x00],
        "scanner": [0x0C, 0x00],
        "radar": [0x0D, 0x00],
    }

    COLORS = {
        "red": 0x01,
        "green": 0x02,
        "yellow": 0x03,
        "blue": 0x04,
        "aqua": 0x05,
        "purple": 0x06,
        "white": 0x07,
    }

    DEFAULT_CONFIG = {
        "effect": "wave-right",
        "speed": 3,
        "brightness": 50,
        "color": "aqua",
    }

    CONFIG_FILE_NAME = "suorafxctl.json"

    def __init__(self):
        self._context = usb1.USBContext()
        self._handle = None
        self._config = dict(self.DEFAULT_CONFIG)

    def acquire(self):
        """Get the access to the device."""

        if not self._handle:
            self._handle = self._context.openByVendorIDAndProductID(
                self.VENDOR_ID,
                self.PRODUCT_ID,
                skip_on_error=True,
            )

        self._handle.detachKernelDriver(self.INTERFACE)
        self._handle.claimInterface(self.INTERFACE)

    def release(self):
        """Release the access to the device."""
        self._handle.releaseInterface(self.INTERFACE)
        self._handle.attachKernelDriver(self.INTERFACE)

    def read_config(self):
        """Read configuration from config file."""
        config_path = os.path.join(
            get_xdg_config_home(),
            self.CONFIG_FILE_NAME,
        )

        if not os.path.isfile(config_path):
            return

        with open(config_path, "r") as file_:
            self._config.update(json.load(file_))

    def write_config(self):
        """Save config to a file."""
        if not os.path.isdir(get_xdg_config_home()):
            os.makedirs(get_xdg_config_home())

        config_path = os.path.join(
            get_xdg_config_home(),
            self.CONFIG_FILE_NAME,
        )

        with open(config_path, "w") as file_:
            json.dump(self._config, file_)

    @property
    def effect(self):
        return self._config["effect"]

    @effect.setter
    def effect(self, value):
        if value not in self.EFFECTS:
            raise ValueError("Unsupported effect '%s'" % value)
        self._config["effect"] = value

    @property
    def speed(self):
        return self._config["speed"]

    @speed.setter
    def speed(self, value):
        if not 0 <= value <= 10:
            raise ValueError("Speed must be an integer between 0 and 10")
        self._config["speed"] = int(value)

    @property
    def brightness(self):
        return self._config["brightness"]

    @brightness.setter
    def brightness(self, value):
        if not 0 <= value <= 50:
            raise ValueError("Brightness must be an integer between 0 and 50")
        self._config["brightness"] = int(value)

    @property
    def color(self):
        return self._config["color"]

    @color.setter
    def color(self, value):
        if value not in self.COLORS:
            raise ValueError("Unsupported color '%s'" % value)
        self._config["color"] = value

    def commit(self):
        "Send the settings to the keyboard."
        self._device_write(
            [
                0x08,
                0x02,
                self.EFFECTS[self.effect][0],
                self.speed,
                self.brightness,
                self.COLORS[self.color],
                self.EFFECTS[self.effect][1],
            ]
        )

    def _calculate_checksum(self, data):
        checksum = 0xFF

        for value in data:
            checksum -= value

        return checksum

    def _device_write(self, data):
        self._handle.controlWrite(
            0x21,
            0x09,
            0x0300,
            0x03,
            bytes(data + [self._calculate_checksum(data)]),
        )


def build_cli():
    cli = argparse.ArgumentParser(
        epilog="The first call to this command will reset all unspecified "
        "settings to their default value"
    )

    cli.add_argument(
        "-e",
        "--effect",
        help="Illumination effect (%s)" % ", ".join(SuoraFX.EFFECTS.keys()),
        choices=SuoraFX.EFFECTS.keys(),
        metavar="EFFECT",
    )

    cli.add_argument(
        "-s",
        "--speed",
        help="Illumination effect speed, from 0 (fast) to 10 (slow)",
        metavar="0-10",
        type=int,
        choices=range(0, 11),
    )

    cli.add_argument(
        "-b",
        "--brightness",
        help="keyboard brightness, from 0 (light off) to 50",
        metavar="0-50",
        type=int,
        choices=range(0, 51),
    )

    cli.add_argument(
        "-c",
        "--color",
        help="Illumination color (%s)" % ", ".join(SuoraFX.COLORS.keys()),
        choices=SuoraFX.COLORS.keys(),
        metavar="COLOR",
    )

    cli.add_argument(
        "-r",
        "--reset",
        help="reset all settings to their default",
        dest="reset",
        action="store_true",
    )

    return cli


def main(args=sys.argv[1:]):
    cli = build_cli()
    settings = cli.parse_args(args)

    suorafx = SuoraFX()

    suorafx.read_config()
    suorafx.acquire()

    if settings.reset:
        suorafx.effect = SuoraFX.DEFAULT_CONFIG["effect"]
        suorafx.speed = SuoraFX.DEFAULT_CONFIG["speed"]
        suorafx.brightness = SuoraFX.DEFAULT_CONFIG["brightness"]
        suorafx.color = SuoraFX.DEFAULT_CONFIG["color"]
    else:
        if settings.effect is not None:
            suorafx.effect = settings.effect
        if settings.speed is not None:
            suorafx.speed = settings.speed
        if settings.brightness is not None:
            suorafx.brightness = settings.brightness
        if settings.color is not None:
            suorafx.color = settings.color

    suorafx.commit()
    suorafx.write_config()
    suorafx.release()


if __name__ == "__main__":
    main()
