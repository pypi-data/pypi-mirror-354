__all__ = ["Supernova"]

from .usb.usb_hid_manager import SUPERNOVA_PID, UsbHidManager

def getConnectedSupernovaDevicesList() -> list:
    '''
    This function can be used to scan all the Supernova devices connected
    to the host computer.

    Arguments
    ---------
    None

    Returns
    -------
    devices: list
        Python list that holds devices dictionary.
    '''

    hwVersionIdentifiers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    hwVersionMask = 0xF000

    fwVersionMajorMask = 0x0F00
    fwVersionMinorMask = 0x00F0
    fwVersionPatchMask = 0x000F

    devices = UsbHidManager.enumerate(SUPERNOVA_PID)

    # For each device, convert the release number to a human-readable format.
    # The release number is a 16-bit number where the first 4 bits are the hardware version,
    # the next 4 bits are the major firmware version, the next 4 bits are the minor firmware version,
    # and the last 4 bits are the patch version.
    # The hardware version is represented by a letter from A to H.
    for device in devices:
        device['hardware_version'] = hwVersionIdentifiers[(device['release_number'] & hwVersionMask) >> 12]
        device['firmware_version'] = f'{(device["release_number"] & fwVersionMajorMask) >> 8}.{(device["release_number"] & fwVersionMinorMask) >> 4}.{(device["release_number"] & fwVersionPatchMask)}'

        # Remove unused fields.
        del device['release_number']
        del device['usage_page']
        del device['usage']
        del device['interface_number']
        # When testing, we encountered that this field was not always present.
        # So we need to check if it exists before deleting it.
        if device.get('bus_type'):
            del device['bus_type']

    return devices