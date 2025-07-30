from ..common_definitions import *

#================================================================================#
# region GPIO COMMAND DEFINITIONS
#================================================================================#

class GpioCommandCodes(Enum):
    """
    Enumeration of GPIO command codes.
    """
    GPIO_CONFIGURE_PIN              = makeCommandCode(Group.GPIO.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 1)
    GPIO_DIGITAL_WRITE              = makeCommandCode(Group.GPIO.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 2)
    GPIO_DIGITAL_READ               = makeCommandCode(Group.GPIO.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 3)
    GPIO_SET_INTERRUPT              = makeCommandCode(Group.GPIO.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 4)
    GPIO_DISABLE_INTERRUPT          = makeCommandCode(Group.GPIO.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 5)
    GPIO_INTERRUPT_NOTIFICATION     = makeCommandCode(Group.GPIO.value, CommandRole.GENERIC.value, CommandType.NOTIFICATION.value, 1)

GPIO_COMMAND_NAMES = {
    result.value: result.name.replace("_", " ") for result in GpioCommandCodes
}

# endregion

#================================================================================#
# region GPIO COMMON DEFINITIONS
#================================================================================#

class GpioPinNumber(Enum):
    """
    This enum represents the possible Gpio Pin Numbers.
    """
    GPIO_1                         = 0x00
    GPIO_2                         = 0x01
    GPIO_3                         = 0x02
    GPIO_4                         = 0x03
    GPIO_5                         = 0x04
    GPIO_6                         = 0x05

class GpioLogicLevel(Enum):
    """
    This enum represents the possible logic levels for Digital I/O.
    """
    LOW                            = 0x00
    HIGH                           = 0x01

class GpioFunctionality(Enum):
    """
    This enum represents the possible functionalities for the GPIO.
    """
    DIGITAL_INPUT                  = 0x00
    DIGITAL_OUTPUT                 = 0x01

class GpioTriggerType(Enum):
    """
    This enum represents the possible Gpio interrupt trigger types.
    """
    TRIGGER_RISING_EDGE             = 0x01
    TRIGGER_FALLING_EDGE            = 0x02
    TRIGGER_BOTH_EDGES              = 0x03

# endregion

#================================================================================#
# region GPIO RESULT DEFINITIONS
#================================================================================#

class GpioResultCodes(Enum):
    """
    Enumeration of GPIO result codes.
    """
    GPIO_NOT_CONFIGURED         = makeResultCode(Group.GPIO.value, 1)
    GPIO_WRONG_CONFIGURATION    = makeResultCode(Group.GPIO.value, 2)

GPIO_RESULT_NAMES = {
    **COMMON_RESULT_NAMES,
    **{result.value: result.name for result in GpioResultCodes}
}

# endregion

#================================================================================#
# region GPIO CONFIGURE PIN
#================================================================================#

# Request ---------------------------------------------------------------------- #

class GpioConfigurePinRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pinNumber", c_uint8),
                ("functionality", c_uint8)]

class GpioConfigurePinRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", GpioConfigurePinRequestParameters_t)]

GpioConfigurePinRequestArray_t = c_uint8 * sizeof(GpioConfigurePinRequestFields_t)

class GpioConfigurePinRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GpioConfigurePinRequestArray_t ),
                ("fields", GpioConfigurePinRequestFields_t )]

# Response --------------------------------------------------------------------- #

class GpioConfigurePinResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

GpioConfigurePinResponseArray_t = c_uint8 * sizeof(GpioConfigurePinResponseFields_t)

class GpioConfigurePinResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", GpioConfigurePinResponseArray_t ),
                ("fields", GpioConfigurePinResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = GpioConfigurePinResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        """
        This function returns a dictionary with the response fields.
        """
        return {
            "id": self.fields.header.id,
            "command": GPIO_COMMAND_NAMES[self.fields.header.code],
            "result": GPIO_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region GPIO DIGITAL WRITE
#================================================================================#

# Request ---------------------------------------------------------------------- #

class GpioDigitalWriteRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pinNumber", c_uint8),
                ("logicLevel", c_uint8)]

class GpioDigitalWriteRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", GpioDigitalWriteRequestParameters_t)]

GpioDigitalWriteRequestArray_t = c_uint8 * sizeof(GpioDigitalWriteRequestFields_t)

class GpioDigitalWriteRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GpioDigitalWriteRequestArray_t ),
                ("fields", GpioDigitalWriteRequestFields_t )]

# Response --------------------------------------------------------------------- #

class GpioDigitalWriteResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

GpioDigitalWriteResponseArray_t = c_uint8 * sizeof(GpioDigitalWriteResponseFields_t)

class GpioDigitalWriteResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", GpioDigitalWriteResponseArray_t ),
                ("fields", GpioDigitalWriteResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = GpioDigitalWriteResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        """
        This function returns a dictionary with the response fields.
        """
        return {
            "id": self.fields.header.id,
            "command": GPIO_COMMAND_NAMES[self.fields.header.code],
            "result": GPIO_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region GPIO DIGITAL READ
#================================================================================#

# Request ---------------------------------------------------------------------- #

class GpioDigitalReadRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pinNumber", c_uint8)]

class GpioDigitalReadRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", GpioDigitalReadRequestParameters_t)]

GpioDigitalReadRequestArray_t = c_uint8 * sizeof(GpioDigitalReadRequestFields_t)

class GpioDigitalReadRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GpioDigitalReadRequestArray_t ),
                ("fields", GpioDigitalReadRequestFields_t )]

# Response --------------------------------------------------------------------- #

class GpioDigitalReadResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("logicLevel", c_uint8)]

class GpioDigitalReadResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", GpioDigitalReadResponseParameters_t)]

GpioDigitalReadResponseArray_t = c_uint8 * sizeof(GpioDigitalReadResponseFields_t)

class GpioDigitalReadResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", GpioDigitalReadResponseArray_t ),
                ("fields", GpioDigitalReadResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = GpioDigitalReadResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        """
        This function returns a dictionary with the response fields.
        """
        return {
            "id": self.fields.header.id,
            "command": GPIO_COMMAND_NAMES[self.fields.header.code],
            "result": GPIO_RESULT_NAMES[self.fields.header.result],
            "logic_level": GpioLogicLevel(self.fields.parameters.logicLevel).name
        }

# endregion

#================================================================================#
# region GPIO SET INTERRUPT
#================================================================================#

# Request ---------------------------------------------------------------------- #

class GpioSetInterruptRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pinNumber", c_uint8),
                ("trigger", c_uint8)]

class GpioSetInterruptRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", GpioSetInterruptRequestParameters_t)]

GpioSetInterruptRequestArray_t = c_uint8 * sizeof(GpioSetInterruptRequestFields_t)

class GpioSetInterruptRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GpioSetInterruptRequestArray_t ),
                ("fields", GpioSetInterruptRequestFields_t )]

# Response --------------------------------------------------------------------- #

class GpioSetInterruptResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

GpioSetInterruptResponseArray_t = c_uint8 * sizeof(GpioSetInterruptResponseFields_t)

class GpioSetInterruptResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", GpioSetInterruptResponseArray_t ),
                ("fields", GpioSetInterruptResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = GpioSetInterruptResponseArray_t.from_buffer_copy(data)


    def toDictionary(self) -> dict:
        """
        This function returns a dictionary with the response fields.
        """
        return {
            "id": self.fields.header.id,
            "command": GPIO_COMMAND_NAMES[self.fields.header.code],
            "result": GPIO_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region GPIO DISABLE INTERRUPT
#================================================================================#

# Request ---------------------------------------------------------------------- #

class GpioDisableInterruptRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pinNumber", c_uint8)]

class GpioDisableInterruptRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", GpioDisableInterruptRequestParameters_t)]

GpioDisableInterruptRequestArray_t = c_uint8 * sizeof(GpioDisableInterruptRequestFields_t)

class GpioDisableInterruptRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GpioDisableInterruptRequestArray_t ),
                ("fields", GpioDisableInterruptRequestFields_t )]

# Response --------------------------------------------------------------------- #

class GpioDisableInterruptResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

GpioDisableInterruptResponseArray_t = c_uint8 * sizeof(GpioDisableInterruptResponseFields_t)

class GpioDisableInterruptResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", GpioDisableInterruptResponseArray_t ),
                ("fields", GpioDisableInterruptResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = GpioDisableInterruptResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        """
        This function returns a dictionary with the response fields.
        """
        return {
            "id": self.fields.header.id,
            "command": GPIO_COMMAND_NAMES[self.fields.header.code],
            "result": GPIO_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region GPIO NOTIFICATION
#================================================================================#

class GpioInterruptNotificationParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pinNumber", c_uint8)]

class GpioInterruptNotificationFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", GpioInterruptNotificationParameters_t)]

gpioInterruptNotificationArray_t = c_uint8 * sizeof(GpioInterruptNotificationFields_t)

class GpioInterruptNotification_t(Union):
    _fields_ = [("data", gpioInterruptNotificationArray_t ),
                ("fields", GpioInterruptNotificationFields_t )]

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": GPIO_COMMAND_NAMES[self.fields.header.code],
            "result": GPIO_RESULT_NAMES[self.fields.header.result],
            "pin_number": GpioPinNumber(self.fields.parameters.pinNumber).name
        }

    def __str__(self) -> str:
        return str(self.toDictionary())

# endregion