import threading
import inspect
import hid

from ..utils.system_message import SystemMessage, SystemOpcode, SystemModules
from .usb_transfer_protocol import USB_FS_INTERRUPT_ENDPOINT_SIZE, USB_HS_INTERRUPT_ENDPOINT_SIZE, UsbTransferProtocol

#================================================================================#
# region Constants definitions
#================================================================================#

ENDPOINT_ID = 0x00

# VID and PID constants definition.
BINHO_VID       = 0x1FC9
SUPERNOVA_PID   = 0x82FC
PULSAR_PID      = 0x82FD

# USB transfer error opcode returned by hidapi write method.
USB_TRANSFER_ERROR_OPCODE = -1

#endregion


#================================================================================#
# region USB HID MANAGER class
#================================================================================#

class UsbHidManager:
    """
    This class is responsible for the management of the USB HID communication. It exposes
    the method to open and close the connections, as well as the method to send data over USB
    to the host adapter. Additionally, it constantly listens to the reception of data and invokes
    the onReceiveCallback every time data is received.

    Attributes
    ----------
    binhoDeviceList: dict
        Class attribute to hold the different Binho devices characteristics.
    thread: threading.Thread
        Thread that is in charge of the data reception.
    run: bool
        Boolean flag used as the variable of control of the thread.
    vendorId: int
        USB Vendor ID
    productId: int
        USB Product ID
    usbHidDevice: hid.device
        Instance of the hid device class which connects withe the low-level HID driver.
    endpointSize: int
        USB Interrupt transfers endpoint size.
    onReceiveCallback:
        Callback function invoked when a new response or notification is received to pass
        the data to the host application.

    """

    # Class attribute.
    binhoDeviceList = {
        SUPERNOVA_PID: USB_FS_INTERRUPT_ENDPOINT_SIZE,
        PULSAR_PID: USB_HS_INTERRUPT_ENDPOINT_SIZE
    }

    @staticmethod
    def enumerate(productId):
        # Get a list of dictionaries of devices info.
        devices = hid.enumerate(BINHO_VID, productId)

        # For each device, print de VID and PID in hex, and convert the path
        # from bytes to String
        for device in devices:
            device['path'] = device['path'].decode(encoding='utf-8')
            device['vendor_id'] = hex(device['vendor_id'])
            device['product_id'] = hex(device['product_id'])

        # Return list of devices.
        return devices

    def __init__(self, productId):

        # Threading
        self.thread = None                                              # Reception thread.
        self.run = False                                                # Variable of thread control.

        # USB specs
        self.vendorId = BINHO_VID                                       # USB Vendor ID.
        self.productId = productId                                      # USB Product ID.
        self.endpointSize = UsbHidManager.binhoDeviceList[productId]    # USB Interrupt transfer endpoint size.
        self.usbHidDevice = hid.device()                                # Instance of hid.device()

        self.transferProtocol = UsbTransferProtocol(self.endpointSize)

        # Responses handling
        self.onReceiveCallback = None                                   # Callback to pass the response/notification received.

    # Private methods --------------------------------------------------------------------------------- #

    def __isRunning(self):
        """
        This method returns True if the reception thread is alive and running.
        """
        return self.thread and self.thread.is_alive() and self.run

    def __stop(self):
        """
        This method ends the USB receiver process and deletes the instance of thread
        so that is possible to create a new instance to reconnect the communication since
        it is not possible to invoke threading.Thread.start() method more than once.
        """
        self.run = False
        if self.thread:
            self.thread.join()
            self.thread = None

    def __start(self):
        """
        This method starts the Thread target function. If a thread is already
        created and running, first ends the current process and starts a new instance since
        it is not possible to invoke threading.Thread.start() method more than once.
        """
        if self.__isRunning():
            self.__stop()

        self.run = True
        self.thread = threading.Thread(target = self.__main, name='USB Receiver', daemon=True)
        self.thread.start()

    def __main(self):
        """
        This method is the Thread target function.
        """
        while self.run == True:
            try:
                # Block for 100 ms to wait for a new message receive in the USB port from the Supernova.
                usbHostAdapterMessage = bytes(self.usbHidDevice.read(self.endpointSize, 100))

                # If new data was received, pass the packet to the USB Transfer Protocol and check if the transfer is complete.
                if usbHostAdapterMessage:
                    transfer = self.transferProtocol.receiveUsbInputTransferPackets(usbHostAdapterMessage)
                    if transfer and self.onReceiveCallback:
                        self.onReceiveCallback(transfer, None)

            except OSError as e:     # This exception is raised from self.usbHostAdapter.read when the Supernova is removed.
                # Create a custom error.
                error = SystemMessage(SystemModules.SYSTEM, SystemOpcode.UNEXPECTED_DISCONNECTION, f"Error {SystemOpcode.UNEXPECTED_DISCONNECTION.name}: Unexpected Supernova disconnection.")
                # Notify to the client.
                self.onReceiveCallback(None, error)
                # Kill process
                self.run = False

    # Public methods --------------------------------------------------------------------------------- #

    def open(self, serial = None, path:str = None):
        """
        This method is in charge of opening the connection with the USB Host Adapter through the HDI API library.

        Parameters
        ----------
        serial: int
            String representing the serial number of the USB Host Adapter.
        path: str
            String representing the OS path of the USB Host Adapter.

        Returns
        -------
        dict:
            A python dictionary representation of a SystemMessage instance. The opcode of the message is:
            - SystemOpcode.OK if the connection with the HID device is completed successfully.
            - SystemOpcode.OPEN_CONNECTION_FAIL if the connection of the HID instance fails.
        """
        # Create response instance.
        sys_response = SystemMessage(SystemModules.SYSTEM, SystemOpcode.OK, "Connection with Supernova device opened successfully.")

        try:
            # Close the connection before reopening it.
            # Stop and kill thread.
            if self.__isRunning():
                self.__stop()

            # Close HID device.
            self.usbHidDevice.close()

            # Open HID connection.
            if path:
                path_bytes = path.encode(encoding='utf-8')
                self.usbHidDevice.open_path(path_bytes)
            else:
                self.usbHidDevice.open(self.vendorId, self.productId, serial)

            # Start thread.
            self.__start()

        except Exception as exc:
            sys_response.opcode = SystemOpcode.OPEN_CONNECTION_FAIL
            sys_response.message = f"Open connection failed. Exception type: {type(exc)}. Exception message: {exc}."

        return sys_response.toDictionary()

    def isRunning(self):
        """
        This method returns True if the USB connection is open and working.
        """
        return self.__isRunning()

    def close(self):
        """
        This method is in charge of closing the connection with the USB Host Adapter through the HDI API library.

        Returns
        -------
        dict:
            A python dictionary representation of a SystemMessage instance. The opcode of the message is:
            - SystemOpcode.OK if the connection with the HID device is closed successfully.
            - SystemOpcode.OPEN_CONNECTION_REQUIRED if the was not previously opened.

        """

        sys_response = SystemMessage(SystemModules.SYSTEM, SystemOpcode.OK, "Communication closed successfully.")

        if self.__isRunning():
            self.__stop()
            # Close HID device.
            self.usbHidDevice.close()
        else:
            sys_response.opcode = SystemOpcode.OPEN_CONNECTION_REQUIRED
            sys_response.message = "It is required to open connection with a Supernova first. Invoke open() method."

        return sys_response.toDictionary()

    def join(self):
        """
        This method waits until the reception thread ends.
        """
        self.thread.join()

    def setOnReceiveCallback(self, callback):
        """
        This function sets the USB receiver callback function.

        Parameters
        ----------
        callback:
            2 parameters signature callback function.

        Returns
        -------
        dict:
            A python dictionary representation of a SystemMessage instance. The opcode of the message is:
            - SystemOpcode.OK if the callback definition is correct and it is assigned to the onReceiveCallback attribute.
            - SystemOpcode.INVALID_CALLBACK_SIGNATURE if the signature of the function is not correct.

        """

        sys_response = SystemMessage(SystemModules.SYSTEM, SystemOpcode.OK, "On event callback function registered successfully.")

        # Get the function signature
        func_signature = inspect.signature(callback)

        # Get the parameters of the function
        func_parameters = func_signature.parameters

        # Check if the function has exactly 2 parameters
        if len(func_parameters) != 2:
            sys_response.opcode = SystemOpcode.INVALID_CALLBACK_SIGNATURE
            sys_response.message = "The function must accept 2 arguments: callback(supernova_response, system_message)."
        else:
            # Save the callback function
            self.onReceiveCallback = callback

        return sys_response.toDictionary()

    def send(self, transfer):
        """
        This method is in charge of sending data to the USB Host Adapter through the HDI API library.

        Parameters
        ----------
        transfers: list
            List of chunks of data to be sent to the USB Host Adapter over USB.

        Returns
        -------
        int:
            An integer representing the result of the USB transfer. The value USB_TRANSFER_ERROR_OPCODE
            represents the transfer failure.

        """

        packets = self.transferProtocol.createUsbOutputTransferPackets(transfer)
        result = 0

        for packet in packets:
            # Prepend ENDPOINT_ID to the transfer
            transfer_with_endpoint = bytes([ENDPOINT_ID]) + packet
            # Send request to USB host adapter
            result = self.usbHidDevice.write(transfer_with_endpoint)

            if result == USB_TRANSFER_ERROR_OPCODE:
                break
        
        return result

#endregion