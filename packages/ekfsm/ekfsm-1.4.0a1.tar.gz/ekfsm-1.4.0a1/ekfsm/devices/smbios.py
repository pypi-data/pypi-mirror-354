from pathlib import Path

from ekfsm.core.components import HWModule
from ekfsm.core.sysfs import SysfsDevice, sysfs_root

from .generic import Device


class SMBIOS(Device):
    """
    A class to represent the SMBIOS device.

    A SMBIOS device is a virtual device that is used to read system
    configuration values from the DMI table.

    Note:
    Currently, only the board version / revision is read from the DMI table.
    """

    def __init__(
        self,
        name: str,
        parent: HWModule | None = None,
        children: list["Device"] | None = None,
        abort: bool = False,
        *args,
        **kwargs,
    ):
        self.sysfs_device: SysfsDevice | None = SysfsDevice(sysfs_root() / Path("devices/virtual/dmi/id"), False)

        super().__init__(name, parent, None, abort, *args, **kwargs)

    def revision(self) -> str:
        """
        Get the board revision from the DMI table.

        Returns
        -------
        str
            The board revision.
        """
        return self.sysfs.read_utf8("board_version")
