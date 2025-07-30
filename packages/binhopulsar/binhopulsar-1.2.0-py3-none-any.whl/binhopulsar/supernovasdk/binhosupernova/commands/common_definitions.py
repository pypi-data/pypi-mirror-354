from abc import abstractmethod
from enum import Enum
from ctypes import *

#================================================================================#
# CONSTANTS DEFINITIONS
#================================================================================#

ID_LSB_INDEX                            = 0
ID_MSB_INDEX                            = 1
COMMAND_CODE_LSB_INDEX                  = 2
COMMAND_CODE_MSB_INDEX                  = 3

#================================================================================#
# region Group Definitions
#================================================================================#

class Group(Enum):
    """
    This enumeration defines the different groups that a command can belong to.
    """
    GLOBAL      = 0
    SYS         = 1
    I2C         = 2
    SPI         = 3
    UART        = 4
    GPIO        = 5
    I3C         = 6
    ONE_WIRE    = 7
    CAN         = 8
    RS485       = 9

# endregion

#================================================================================#
# region Command Codes Definitions
#================================================================================#

class CommandRole(Enum):
    """
    This enumeration defines the different roles that a command can have.
    """
    GENERIC = 0
    CONTROLLER = 1
    TARGET = 2

class CommandType(Enum):
    """
    This enumeration defines the different types that a command can have.
    """
    REQUEST_RESPONSE = 0
    NOTIFICATION = 1

COMMAND_GROUP_MASK  = 0xFC00
COMMAND_ROLE_MASK   = 0x0300
COMMAND_TYPE_MASK   = 0x0080

COMMAND_GROUP_SHIFT = 10
COMMAND_ROLE_SHIFT  = 8
COMMAND_TYPE_SHIFT  = 7

def makeCommandCode(group, role, type, value):
    """
    This function creates a command code based on the group, role, type and value.
    """
    return ((group << COMMAND_GROUP_SHIFT) | (role << COMMAND_ROLE_SHIFT) | (type << COMMAND_TYPE_SHIFT) | value)

def getCommandGroup(commandCode):
    """
    This function returns the group of a command code.
    """
    return ((commandCode & COMMAND_GROUP_MASK) >> COMMAND_GROUP_SHIFT)

def getCommandRole(commandCode):
    """
    This function returns the role of a command code.
    """
    return ((commandCode & COMMAND_ROLE_MASK) >> COMMAND_ROLE_SHIFT)

def getCommandType(commandCode):
    """
    This function returns the type of a command code.
    """
    return ((commandCode & COMMAND_TYPE_MASK) >> COMMAND_TYPE_SHIFT)

# endregion

#================================================================================#
# region Result Codes Definitions
#================================================================================#

RESULT_GROUP_MASK   = 0xFF00
RESULT_GROUP_SHIFT  = 8

def makeResultCode(group, value):
    """
    This function creates a result code based on the group and value.
    """
    return ((group << RESULT_GROUP_SHIFT) | value)

def getResultGroup(resultCode):
    """
    This function returns the group of a result code.
    """
    return ((resultCode & RESULT_GROUP_MASK) >> RESULT_GROUP_SHIFT)

class CommonResultCodes(Enum):
    """
    Enumeration of the common result codes.
    """
    SUCCESS                             = makeResultCode(Group.GLOBAL.value, 0)
    UNSUPPORTED_COMMAND                 = makeResultCode(Group.GLOBAL.value, 1)
    INVALID_COMMAND                     = makeResultCode(Group.GLOBAL.value, 2)
    FULL_RECEPTION_QUEUE                = makeResultCode(Group.GLOBAL.value, 3)
    INVALID_PARAMETER                   = makeResultCode(Group.GLOBAL.value, 4)
    FEATURE_NOT_SUPPORTED_BY_HARDWARE   = makeResultCode(Group.GLOBAL.value, 5)
    INTERFACE_NOT_INITIALIZED           = makeResultCode(Group.GLOBAL.value, 6)
    INTERFACE_ALREADY_INITIALIZED       = makeResultCode(Group.GLOBAL.value, 7)
    BUS_NOT_SUPPORTED                   = makeResultCode(Group.GLOBAL.value, 8)
    BUS_TIMEOUT                         = makeResultCode(Group.GLOBAL.value, 9)
    RX_FIFO_FULL                        = makeResultCode(Group.GLOBAL.value, 10)
    TX_FIFO_EMPTY                       = makeResultCode(Group.GLOBAL.value, 11)
    UNHANDLED_ERROR                     = makeResultCode(Group.GLOBAL.value, 12)

COMMON_RESULT_NAMES = {
    result.value: result.name for result in CommonResultCodes
}

# endregion

#================================================================================#
# region Command Request definitions
#================================================================================#

class CommandRequestHeader_t(Structure):
    """
    Command request header structure representation.

    This struct contains the different fields that compose a command
    request header.
    """
    _pack_ = 1
    _fields_ = [("id", c_uint16),
                ("code", c_uint16)]

class BaseCommandRequest_t(Union):
    """ Base class for all the command request classes."""

    def toBytes(self) -> bytes:
        """
        Method to return an bytes object representing the command
        serialization.
        """
        if hasattr(self, 'data'):
            return bytes(self.data)

# endregion

#================================================================================#
# region Command Response definitions
#================================================================================#

class CommandResponseHeader_t(Structure):
    """
    Command response header structure representation.

    This struct contains the different fields that compose a command
    response header.
    """
    _pack_ = 1
    _fields_ = [("id", c_uint16),
                ("code", c_uint16),
                ("result", c_uint16)]

class BaseCommandResponse_t(Union):
    """ Base class for all the command response classes."""

    @abstractmethod
    def fromBytes(self, data):
        """
        Abstract method that must be implemented by subclasses
        to populate the command response fields from a serialized
        bytes object.
        """
        pass

    @abstractmethod
    def toDictionary(self) -> bytes:
        """
        Abstract method that must be implemented by subclasses
        to serialize the union into a bytes object.
        """
        pass

    def __str__(self) -> str:
        """
        This method creates the string representation of the dictionary
        representation of the command responses.
        """
        return str(self.toDictionary())

# endregion

#================================================================================#
# region Notification definitions
#================================================================================#

class NotificationHeader_t(Structure):
    """
    Notification header structure representation.

    This struct contains the different fields that compose an asynchronous
    notification.
    """
    _pack_ = 1
    _fields_ = [("id", c_uint16),
                ("code", c_uint16),
                ("result", c_uint16)]

# endregion