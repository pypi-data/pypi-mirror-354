from ..common_definitions import *

#================================================================================#
# region UART COMMAND DEFINITIONS
#================================================================================#

class UartCommandCodes(Enum):
    """
    Enumerator of the UART command codes.
    """
    UART_DEINIT                 = makeCommandCode(Group.UART.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 1)
    UART_INIT                   = makeCommandCode(Group.UART.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 2)
    UART_SET_PARAMETERS         = makeCommandCode(Group.UART.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 3)
    UART_GET_PARAMETERS         = makeCommandCode(Group.UART.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 4)
    UART_SEND                   = makeCommandCode(Group.UART.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 5)
    UART_RECEIVE_NOTIFICATION	= makeCommandCode(Group.UART.value, CommandRole.GENERIC.value, CommandType.NOTIFICATION.value, 1)

UART_COMMAND_NAMES = {
    result.value: result.name.replace("_", " ") for result in UartCommandCodes
}

# endregion

#================================================================================#
# region UART COMMON DEFINITIONS
#================================================================================#

# UART Bus Configuration
class UartBaudRate(Enum):
    """
    This enum represents the UART baudrate options.
    """
    UART_BAUD_600    = 0x00
    UART_BAUD_1200   = 0x01
    UART_BAUD_2400   = 0x02
    UART_BAUD_4800   = 0x03
    UART_BAUD_9600   = 0x04
    UART_BAUD_14400  = 0x05
    UART_BAUD_19200  = 0x06
    UART_BAUD_38400  = 0x07
    UART_BAUD_56000  = 0x08
    UART_BAUD_57600  = 0x09
    UART_BAUD_115200 = 0x0A

class UartParity(Enum):
    """ 
    This enum represents the UART parity options.
    """
    UART_NO_PARITY   = 0x00
    UART_EVEN_PARITY = 0x01
    UART_ODD_PARITY  = 0x02

class UartDataSize(Enum):
    """
    This enum represents the UART data character size options.
    """
    UART_7BIT_BYTE = 0x00
    UART_8BIT_BYTE = 0x01

class UartStopBit(Enum):
    """
    This enum represents the UART stop bit options.
    """
    UART_ONE_STOP_BIT = 0x00
    UART_TWO_STOP_BIT = 0x01

class UartConfigurationParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("baudRate", c_uint8),
                ("hardwareHandshake", c_uint8),
                ("parityMode", c_uint8),
                ("dataSize", c_uint8),
                ("stopBitType", c_uint8)]

# endregion

#================================================================================#
# region UART INIT
#================================================================================#

# Request ---------------------------------------------------------------------- #

class UartInitRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", UartConfigurationParameters_t)]

UartInitRequestArray_t = c_uint8 * sizeof(UartInitRequestFields_t)

class UartInitRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", UartInitRequestArray_t),
                ("fields", UartInitRequestFields_t)]

# Response --------------------------------------------------------------------- #

class UartInitResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

UartInitResponseArray_t = c_uint8 * sizeof(UartInitResponseFields_t)

class UartInitResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", UartInitResponseArray_t ),
                ("fields", UartInitResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = UartInitResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": UART_COMMAND_NAMES[self.fields.header.code],
            "result": COMMON_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region UART SET PARAMETERS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class UartSetParametersRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", UartConfigurationParameters_t)]

UartSetParametersRequestArray_t = c_uint8 * sizeof(UartSetParametersRequestFields_t)

class UartSetParametersRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", UartSetParametersRequestArray_t),
                ("fields", UartSetParametersRequestFields_t)]

# Response --------------------------------------------------------------------- #

class UartSetParametersResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

UartSetParametersResponseArray_t = c_uint8 * sizeof(UartSetParametersResponseFields_t)

class UartSetParametersResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", UartSetParametersResponseArray_t ),
                ("fields", UartSetParametersResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = UartSetParametersResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": UART_COMMAND_NAMES[self.fields.header.code],
            "result": COMMON_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region UART SEND
#================================================================================#

MAX_UART_TRANSFER_LENGTH = 1024

# Request ---------------------------------------------------------------------- #

class UartSendRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("payloadLength", c_uint16)]

UartSendRequestPayload_t = c_uint8 * MAX_UART_TRANSFER_LENGTH

class UartSendRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", UartSendRequestParameters_t),
                ("payload", UartSendRequestPayload_t)]

UartSendRequestArray_t = c_uint8 * sizeof(UartSendRequestFields_t)

class UartSendRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", UartSendRequestArray_t),
                ("fields", UartSendRequestFields_t)]

    def toBytes(self) -> bytes:
        """
        Method to return an bytes object representing the command
        serialization.
        """
        length = sizeof(CommandRequestHeader_t) + sizeof(UartSendRequestParameters_t) + self.fields.parameters.payloadLength
        return bytes(self.data[:length])

# Response --------------------------------------------------------------------- #

class UartSendResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

UartSendResponseArray_t = c_uint8 * sizeof(UartSendResponseFields_t)

class UartSendResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", UartSendResponseArray_t),
                ("fields", UartSendResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = UartSendResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": UART_COMMAND_NAMES[self.fields.header.code],
            "result": COMMON_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region UART RECEIVE NOTIFICATION
#================================================================================#

class UartReceiveNotificationParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("payloadLength", c_uint16)]

UartReceiveNotificationPayload_t = c_uint8 * MAX_UART_TRANSFER_LENGTH

class UartReceiveNotificationFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", UartReceiveNotificationParameters_t),
                ("payload", UartReceiveNotificationPayload_t)]

UartReceiveNotificationArray_t = c_uint8 * sizeof(UartReceiveNotificationFields_t)

class UartReceiveNotification_t(Union):
    _fields_ = [("data", UartReceiveNotificationArray_t),
                ("fields", UartReceiveNotificationFields_t)]

    def fromBytes(self, data):
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": UART_COMMAND_NAMES[self.fields.header.code],
            "result": COMMON_RESULT_NAMES[self.fields.header.result],
            "payload_length": self.fields.parameters.payloadLength,
            "payload": self.fields.payload[:self.fields.parameters.payloadLength]
        }

    def __str__(self) -> str:
        return str(self.toDictionary())

# endregion