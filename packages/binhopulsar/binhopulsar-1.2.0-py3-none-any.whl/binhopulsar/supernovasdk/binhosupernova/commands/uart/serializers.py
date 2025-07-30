from .definitions import *

def uartInitSerializer(id: c_uint16, baudrate: UartBaudRate, hardwareHandshake:bool, parityMode:UartParity, dataSize:UartDataSize, stopBit: UartStopBit) -> tuple[bytes, UartInitResponse_t]:
    """
    This function creates the associated command for the UART INIT command to send to the USB HID device.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    baudrate : UartBaudRate
        This parameter represents the UART TX and RX frequency from the options provided by the UartBaudRate enum.
        The frequency goes from 600bps to up to 115200bps.
    hardwareHandshake : bool
        This parameter represents a boolean flag to enable or disable this option.
    parityMode: UartParity
        This parameter represents the different parity modes available in the UartParity enum.
        The parity modes are: none, even or odd.
    dataSize: UartDataSize
        This parameter represents the different data sizes available in the UartDataSize enum.
        The data sizes are either 7 or 8.
    stopBit: UartStopBit
        This parameter represent the different stop bit configuration available in the UartStopBit enum.
        The stop bit can be of size 1 or 2.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command descriptor
    command = UartInitRequest_t()

    # Set endpoint ID and command opcode.
    command.fields.header.id = id
    command.fields.header.code = UartCommandCodes.UART_INIT.value
    command.fields.parameters.baudRate = baudrate.value
    command.fields.parameters.hardwareHandshake = hardwareHandshake
    command.fields.parameters.parityMode = parityMode.value
    command.fields.parameters.dataSize = dataSize.value
    command.fields.parameters.stopBitType = stopBit.value

    return command.toBytes(), UartInitResponse_t()

def uartSetParametersSerializer(id: c_uint16, baudrate: UartBaudRate, hardwareHandshake:bool, parityMode:UartParity, dataSize:UartDataSize, stopBit: UartStopBit) -> tuple[bytes, UartSetParametersResponse_t]:
    """
    This function creates the associated command for the UART SET PARAMETERS command to send to the USB HID device.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    baudrate : UartBaudRate
        This parameter represents the UART TX and RX frequency from the options provided by the UartBaudRate enum.
        The frequency goes from 600bps to up to 115200bps.
    hardwareHandshake : bool
        This parameter represents a boolean flag to enable or disable this option.
    parityMode: UartParity
        This parameter represents the different parity modes available in the UartParity enum.
        The parity modes are: none, even or odd.
    dataSize: UartDataSize
        This parameter represents the different data sizes available in the UartDataSize enum.
        The data sizes are either 7 or 8.
    stopBit: UartStopBit
        This parameter represent the different stop bit configuration available in the UartStopBit enum.
        The stop bit can be of size 1 or 2.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command descriptor
    command = UartSetParametersRequest_t()

    # Set endpoint ID and command opcode.
    command.fields.header.id = id
    command.fields.header.code = UartCommandCodes.UART_SET_PARAMETERS.value
    command.fields.parameters.baudRate = baudrate.value
    command.fields.parameters.hardwareHandshake = hardwareHandshake
    command.fields.parameters.parityMode = parityMode.value
    command.fields.parameters.dataSize = dataSize.value
    command.fields.parameters.stopBitType = stopBit.value

    return command.toBytes(), UartSetParametersResponse_t()


def uartSendSerializer(id: c_uint16, payload: list) -> tuple[bytes, UartSendResponse_t]:
    """
    Generate the UART SEND command.

    Arguments
    ---------
    id: c_uint16
        ID that identifies the transaction.
    payload: list
        Data to be sent.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = UartSendRequest_t()

    # Set endpoint ID and command opcode.
    command.fields.header.id = id
    command.fields.header.code = UartCommandCodes.UART_SEND.value
    command.fields.parameters.payloadLength = len(payload)

    # Load Payload
    for i in range(command.fields.parameters.payloadLength):
        command.fields.payload[i] = payload[i]

    # Return command
    return command.toBytes(), UartSendResponse_t()