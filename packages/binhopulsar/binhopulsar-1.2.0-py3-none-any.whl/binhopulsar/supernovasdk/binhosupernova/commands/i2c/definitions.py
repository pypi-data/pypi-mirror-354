from ..common_definitions import *

#================================================================================#
# region I2C COMMAND DEFINITIONS
#================================================================================#

class I2cCommandCodes(Enum):
    """
    Enumeration of I2C command codes.
    """
    I2C_DEINIT                      = makeCommandCode(Group.I2C.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 1)
    I2C_SET_PULLUP_RESISTORS        = makeCommandCode(Group.I2C.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 2)
    I2C_CONTROLLER_INIT             = makeCommandCode(Group.I2C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 1)
    I2C_CONTROLLER_SET_PARAMETERS   = makeCommandCode(Group.I2C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 2)
    I2C_CONTROLLER_GET_PARAMETERS   = makeCommandCode(Group.I2C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 3)
    I2C_CONTROLLER_WRITE            = makeCommandCode(Group.I2C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 4)
    I2C_CONTROLLER_READ             = makeCommandCode(Group.I2C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 5)
    I2C_CONTROLLER_SCAN_BUS         = makeCommandCode(Group.I2C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 6)

I2C_COMMAND_NAMES = {
    result.value: result.name.replace("_", " ") for result in I2cCommandCodes
}

# endregion

#================================================================================#
# region I2C COMMON DEFINITIONS
#================================================================================#

# I2C Bus Configuration
I2C_CONTROLLER_MIN_FREQUENCY = 100000
I2C_CONTROLLER_MAX_FREQUENCY = 1000000

class I2cPullUpResistorsValue(Enum):
    """
    This enum represents the total value of the I2C Pull-Up resistors
    """
    I2C_PULLUP_150Ohm  = 0x00
    I2C_PULLUP_220Ohm  = 0x01
    I2C_PULLUP_330Ohm  = 0x02
    I2C_PULLUP_470Ohm  = 0x03
    I2C_PULLUP_680Ohm  = 0x04
    I2C_PULLUP_1kOhm   = 0x05
    I2C_PULLUP_1_5kOhm = 0x06
    I2C_PULLUP_2_2kOhm = 0x07
    I2C_PULLUP_3_3kOhm = 0x08
    I2C_PULLUP_4kOhm   = 0x09
    I2C_PULLUP_4_7kOhm = 0x0A
    I2C_PULLUP_10kOhm  = 0x0B
    I2C_PULLUP_DISABLE = 0x0C

class I2cBus(Enum):
    """
    This enum represent the I2C selected bus
    """
    I2C_BUS_A = 0x00
    I2C_BUS_B = 0x01

# Definitions for I2C address validation
I2C_MIN_ADDRESS = 0x00
I2C_MAX_10_BIT_ADDRESS = 0x3FF

# Definitions for 10-bit I2C address
I2C_10_BIT_ADDRESS_FIRST_BYTE_MASK  = 0x78
I2C_10_BIT_ADDRESS_FIRST_BYTE_SHIFT = 8
I2C_10_BIT_ADDRESS_SECOND_BYTE_MASK = 0xFF

# Definitions for I2C register address
I2C_7_BIT_REGISTER_ADDRESS_MAX_LENGTH = 4
I2C_10_BIT_REGISTER_ADDRESS_MAX_LENGTH = 3

# endregion

#================================================================================#
# region I2C RESULT DEFINITIONS
#================================================================================#

class I2cResultCodes(Enum):
    """
    Enumeration of I2C result codes.
    """
    I2C_PULLUP_RESISTOR_SETTING_FAILURE = makeResultCode(Group.I2C.value, 1)
    I2C_ARBITRATION_LOST				= makeResultCode(Group.I2C.value, 2)
    I2C_NACK_ADDRESS					= makeResultCode(Group.I2C.value, 3)
    I2C_NACK_BYTE						= makeResultCode(Group.I2C.value, 4)
    I2C_BIT_ERROR						= makeResultCode(Group.I2C.value, 5)
    I2C_START_STOP_ERROR				= makeResultCode(Group.I2C.value, 6)
    I2C_BUSY							= makeResultCode(Group.I2C.value, 7)
    I2C_TIMEOUT_CONTINUE_TRANSFER		= makeResultCode(Group.I2C.value, 8)
    I2C_TIMEOUT_WAITING_BUS_EVENT		= makeResultCode(Group.I2C.value, 9)
    I2C_TIMEOUT_SCL_LOW					= makeResultCode(Group.I2C.value, 10)
    I2C_DMA_REQUEST_FAIL				= makeResultCode(Group.I2C.value, 11)
    I2C_INVALID_PARAMETER				= makeResultCode(Group.I2C.value, 12) 
    I2C_NO_TRANSFER_IN_PROGRESS			= makeResultCode(Group.I2C.value, 13)
    I2C_UNEXPECTED_STATE				= makeResultCode(Group.I2C.value, 14)
    I2C_BUS_WITH_NO_TARGETS_CONNECTED   = makeResultCode(Group.I2C.value, 15)

I2C_RESULT_NAMES = {
    **COMMON_RESULT_NAMES,
    **{result.value: result.name for result in I2cResultCodes}
}

# endregion

#================================================================================#
# region I2C CONTROLLER INIT
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I2cControllerInitRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8),
                ("frequency_Hz", c_uint32),
                ("pullUpValue", c_uint8)]

class I2cControllerInitRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I2cControllerInitRequestParameters_t)]

I2cControllerInitRequestArray_t = c_uint8 * sizeof(I2cControllerInitRequestFields_t)

class I2cControllerInitRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I2cControllerInitRequestArray_t ),
                ("fields", I2cControllerInitRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I2cControllerInitResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8)]

class I2cControllerInitResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I2cControllerInitResponseParameters_t)]

I2cControllerInitResponseArray_t = c_uint8 * sizeof(I2cControllerInitResponseFields_t)

class I2cControllerInitResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I2cControllerInitResponseArray_t ),
                ("fields", I2cControllerInitResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I2cControllerInitResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I2C_COMMAND_NAMES[self.fields.header.code],
            "result": I2C_RESULT_NAMES[self.fields.header.result],
            "i2c_bus": I2cBus(self.fields.parameters.busId).name
        }

# endregion

#================================================================================#
# region I2C CONTROLLER SET PARAMETERS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I2cControllerSetParametersRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8),
                ("frequency_Hz", c_uint32),
                ("pullUpValue", c_uint8)]

class I2cControllerSetParametersRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I2cControllerSetParametersRequestParameters_t)]

I2cControllerSetParametersRequestArray_t = c_uint8 * sizeof(I2cControllerSetParametersRequestFields_t)

class I2cControllerSetParametersRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I2cControllerSetParametersRequestArray_t ),
                ("fields", I2cControllerSetParametersRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I2cControllerSetParametersResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8)]

class I2cControllerSetParametersResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I2cControllerSetParametersResponseParameters_t)]

I2cControllerSetParametersResponseArray_t = c_uint8 * sizeof(I2cControllerSetParametersResponseFields_t)

class I2cControllerSetParametersResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I2cControllerSetParametersResponseArray_t ),
                ("fields", I2cControllerSetParametersResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I2cControllerSetParametersResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I2C_COMMAND_NAMES[self.fields.header.code],
            "result": I2C_RESULT_NAMES[self.fields.header.result],
            "i2c_bus": I2cBus(self.fields.parameters.busId).name,
        }

# endregion

#================================================================================#
# region I2C SET PULL UP RESISTORS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I2cSetPullUpResistorsRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8),
    			("pullUpValue", c_uint8)]

class I2cSetPullUpResistorsRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I2cSetPullUpResistorsRequestParameters_t)]

I2cSetPullUpResistorsRequestArray_t = c_uint8 * sizeof(I2cSetPullUpResistorsRequestFields_t)

class I2cSetPullUpResistorsRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I2cSetPullUpResistorsRequestArray_t ),
                ("fields", I2cSetPullUpResistorsRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I2cSetPullUpResistorsResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8)]

class I2cSetPullUpResistorsResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I2cSetPullUpResistorsResponseParameters_t)]

I2cSetPullUpResistorsResponseArray_t = c_uint8 * sizeof(I2cSetPullUpResistorsResponseFields_t)

class I2cSetPullUpResistorsResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I2cSetPullUpResistorsResponseArray_t ),
                ("fields", I2cSetPullUpResistorsResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I2cSetPullUpResistorsResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I2C_COMMAND_NAMES[self.fields.header.code],
            "result": I2C_RESULT_NAMES[self.fields.header.result],
            "i2c_bus": I2cBus(self.fields.parameters.busId).name,
        }

# endregion

#================================================================================#
# region I2C CONTROLLER TRANSFER
#================================================================================#

MAX_I2C_TRANSFER_LENGTH = 1024

# Request ---------------------------------------------------------------------- #

class I2cControllerTransferRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8),
    			("transfLength", c_uint16),
                ("targetAddress", c_uint8),
                ("registerAddressLength", c_uint8),
                ("registerAddress", c_uint32),
                ("isNonStop", c_uint8)]

I2cControllerTransferRequestPayload_t = c_uint8 * MAX_I2C_TRANSFER_LENGTH

class I2cControllerTransferRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I2cControllerTransferRequestParameters_t),
                ("payload", I2cControllerTransferRequestPayload_t)]

I2cControllerTransferRequestArray_t = c_uint8 * sizeof(I2cControllerTransferRequestFields_t)

class I2cControllerTransferRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I2cControllerTransferRequestArray_t),
                ("fields", I2cControllerTransferRequestFields_t )]

    def toBytes(self) -> bytes:
        """
        Method to return an bytes object representing the command
        serialization.
        """
        length = sizeof(CommandRequestHeader_t) + sizeof(I2cControllerTransferRequestParameters_t)

        if self.fields.header.code == I2cCommandCodes.I2C_CONTROLLER_WRITE.value:
            length += self.fields.parameters.transfLength

        return bytes(self.data[:length])

# Response --------------------------------------------------------------------- #

class I2cControllerTransferResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8),
    			("payloadLength", c_uint16)]

I2cControllerTransferResponsePayload_t = c_uint8 * MAX_I2C_TRANSFER_LENGTH

class I2cControllerTransferResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I2cControllerTransferResponseParameters_t),
                ("payload", I2cControllerTransferResponsePayload_t)]

I2cControllerTransferResponseArray_t = c_uint8 * sizeof(I2cControllerTransferResponseFields_t)

class I2cControllerTransferResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I2cControllerTransferResponseArray_t ),
                ("fields", I2cControllerTransferResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:
        response = {
            "id": self.fields.header.id,
            "command": I2C_COMMAND_NAMES[self.fields.header.code],
            "result": I2C_RESULT_NAMES[self.fields.header.result],
            "i2c_bus": I2cBus(self.fields.parameters.busId).name,
            "payload_length": self.fields.parameters.payloadLength,
        }

        if self.fields.header.code == I2cCommandCodes.I2C_CONTROLLER_READ.value:
            response["payload"] = self.fields.payload[:self.fields.parameters.payloadLength]
        
        return response

# endregion

#================================================================================#
# region I2C CONTROLLER SCAN BUS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I2cControllerScanBusRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8),
                ("include10BitAddresses", c_uint8)]

class I2cControllerScanBusRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I2cControllerScanBusRequestParameters_t)]
    
I2cControllerScanBusRequestArray_t = c_uint8 * sizeof(I2cControllerScanBusRequestFields_t)

class I2cControllerScanBusRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I2cControllerScanBusRequestArray_t),
                ("fields", I2cControllerScanBusRequestFields_t)]
    
# Response --------------------------------------------------------------------- #

I2C_CONTROLLER_SCAN_BUS_PAYLOAD_LENGTH = 100

class I2cControllerScanBusResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("busId", c_uint8),
                ("count7BitAddresses", c_uint8),
                ("count10BitAddresses", c_uint8)]

I2cControllerScanBusResponsePayload_t = c_uint8 * I2C_CONTROLLER_SCAN_BUS_PAYLOAD_LENGTH

class I2cControllerScanBusResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I2cControllerScanBusResponseParameters_t),
                ("payload", I2cControllerScanBusResponsePayload_t)]

I2cControllerScanBusResponseArray_t = c_uint8 * sizeof(I2cControllerScanBusResponseFields_t)

class I2cControllerScanBusResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I2cControllerScanBusResponseArray_t),
                ("fields", I2cControllerScanBusResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def __formatDetected10BitAddresses(self, rawData, count):
        """
        This function formats the byte list of detected 10-bit addresses into a list of uint16_t.
        """
        addresses = []
        for i in range(count):
            address = (rawData[2*i + 1] << 8) | rawData[2*i]
            addresses.append(address)
        return addresses

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I2C_COMMAND_NAMES[self.fields.header.code],
            "result": I2C_RESULT_NAMES[self.fields.header.result],
            "i2c_bus": I2cBus(self.fields.parameters.busId).name,
            "detected_7_bit_addresses": self.fields.payload[:self.fields.parameters.count7BitAddresses],
            "detected_10_bit_addresses": self.__formatDetected10BitAddresses(self.fields.payload[self.fields.parameters.count7BitAddresses:], self.fields.parameters.count10BitAddresses)
        }

# endregion