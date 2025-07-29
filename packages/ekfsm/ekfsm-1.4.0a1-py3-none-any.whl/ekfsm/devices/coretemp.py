from __future__ import annotations

import glob
import os
from pathlib import Path

import ekfsm.core
from ekfsm.core.sysfs import sysfs_root
from ekfsm.devices.generic import Device

# Path to the root of the HWMON sysfs filesystem
HWMON_ROOT = sysfs_root() / Path("class/hwmon")


def find_core_temp_dir(hwmon_dir) -> Path:
    """
    Find the directory containing the coretemp hwmon device.

    Args:
        hwmon_dir: Path to the hwmon directory

    Returns:
        Path to the directory containing the coretemp hwmon device

    Raises:
        FileNotFoundError: If no coretemp directory is found
    """
    # List all 'name' files in each subdirectory of hwmon_dir
    name_files = glob.glob(os.path.join(hwmon_dir, "*", "name"))

    # Search for the file containing "coretemp"
    for name_file in name_files:
        with open(name_file, "r") as file:
            if file.readline().strip() == "coretemp":
                # Return the directory containing this file
                return Path(os.path.dirname(name_file))

    raise FileNotFoundError("No coretemp directory found")


class CoreTemp(Device):
    """
    This class provides an interface to read the CPU core temperature from the HWMON device.

    Note:
    Currently, only the average temperature over all cores is read from the HWMON device.
    """

    def __init__(
        self,
        name: str,
        parent: Device,
        children: list["Device"] | None = None,
        abort: bool = False,
        *args,
        **kwargs,
    ):
        dir = find_core_temp_dir(sysfs_root() / Path("class/hwmon"))
        self.sysfs_device = ekfsm.core.sysfs.SysfsDevice(dir, False)

        super().__init__(name, parent, None, abort, *args, **kwargs)

    def cputemp(self):
        """
        Get the CPU temperature from the HWMON device.

        Returns
        -------
        int
            The CPU temperature in degrees Celsius.
        """
        return self.sysfs.read_int("temp1_input") / 1000
