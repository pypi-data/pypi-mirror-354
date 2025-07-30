__all__ = ["Pulsar"]

from .supernovasdk.binhosupernova import getConnectedSupernovaDevicesList

def getConnectedPulsarDevicesList() -> list:
    '''
    This function can be used to scan all the Pulsar devices connected
    to the host computer.

    Arguments
    ---------
    None

    Returns
    -------
    devices: list
        Python list that holds devices dictionary.
    '''
    # Return list of devices.
    return getConnectedSupernovaDevicesList()
