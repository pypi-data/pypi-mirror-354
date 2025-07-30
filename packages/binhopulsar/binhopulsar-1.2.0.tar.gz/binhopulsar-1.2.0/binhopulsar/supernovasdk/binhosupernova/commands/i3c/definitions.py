from ..common_definitions import *

#================================================================================#
# region I3C CONSTANTS DEFINITIONS
#================================================================================#

MAX_REGISTER_ADDRESS_LENGTH     = 4         # Maximum length of register addresses
MAX_I3C_PRIVATE_TRANSFER_LENGTH = 1024      # Maximum I3C Private Transfer length
MAX_I3C_CCC_TRANSFER_LENGTH     = 255       # Maximum I3C CCC Transfer length
MAX_I3C_IBI_PAYLOAD_LENGTH      = 8         # Maximum IBI Payload Length.

#endregion

#================================================================================#
# region I3C COMMAND DEFINITIONS
#================================================================================#

class I3cCommandCodes(Enum):
    """
    Enumeration of I3C command codes.
    """
    I3C_DEINIT                                  = makeCommandCode(Group.I3C.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 1)
    I3C_SET_PULLUP_RESISTORS                    = makeCommandCode(Group.I3C.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 2)
    I3C_CONTROLLER_INIT                         = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 1)
    I3C_CONTROLLER_SET_PARAMETERS               = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 2)
    I3C_CONTROLLER_GET_PARAMETERS               = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 3)
    I3C_CONTROLLER_INIT_BUS                     = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 4)
    I3C_CONTROLLER_RESET_BUS                    = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 5)
    I3C_CONTROLLER_GET_TARGET_DEVICES_TABLE     = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 6)
    I3C_CONTROLLER_SET_TARGET_DEVICE_CONFIG     = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 7)
    I3C_CONTROLLER_PRIVATE_TRANSFER             = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 8)
    I3C_CONTROLLER_CCC_TRANSFER                 = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 9)
    I3C_CONTROLLER_TRIGGER_PATTERN              = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 10)
    I3C_CONTROLLER_IBI_REQUEST_NOTIFICATION     = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.NOTIFICATION.value, 1)
    I3C_CONTROLLER_HJ_REQUEST_NOTIFICATION      = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.NOTIFICATION.value, 2)
    I3C_CONTROLLER_CR_REQUEST_NOTIFICATION      = makeCommandCode(Group.I3C.value, CommandRole.CONTROLLER.value, CommandType.NOTIFICATION.value, 3)
    I3C_TARGET_INIT                             = makeCommandCode(Group.I3C.value, CommandRole.TARGET.value, CommandType.REQUEST_RESPONSE.value, 1)
    I3C_TARGET_SET_PARAMETERS                   = makeCommandCode(Group.I3C.value, CommandRole.TARGET.value, CommandType.REQUEST_RESPONSE.value, 2)
    I3C_TARGET_WRITE_MEMORY                     = makeCommandCode(Group.I3C.value, CommandRole.TARGET.value, CommandType.REQUEST_RESPONSE.value, 3)
    I3C_TARGET_READ_MEMORY                      = makeCommandCode(Group.I3C.value, CommandRole.TARGET.value, CommandType.REQUEST_RESPONSE.value, 4)
    I3C_TARGET_BUS_EVENT_NOTIFICATION           = makeCommandCode(Group.I3C.value, CommandRole.TARGET.value, CommandType.NOTIFICATION.value, 1)

I3C_COMMAND_NAMES = {
    result.value: result.name.replace("_", " ") for result in I3cCommandCodes
}

# endregion

#================================================================================#
# region I3C RESULT DEFINITIONS
#================================================================================#

class I3cResultCodes(Enum):
    """
    Enumeration of I3C result codes.
    """
    FULL_TARGET_DEVICES_TABLE 					= makeResultCode(Group.I3C.value,1)
    NOT_ENOUGH_SPACE_IN_TARGET_DEVICES_TABLE 	= makeResultCode(Group.I3C.value,2)
    TARGET_DEVICES_TABLE_OVERFLOW 				= makeResultCode(Group.I3C.value,3)
    TARGET_ADDRESS_NOT_FOUND_IN_THE_TABLE 		= makeResultCode(Group.I3C.value,4)
    REPEATED_TARGET_ADDRESS 					= makeResultCode(Group.I3C.value,5)
    INVALID_TARGET_ADDRESS 						= makeResultCode(Group.I3C.value,6)
    I3C_BUS_INIT_NACK_RSTDAA 					= makeResultCode(Group.I3C.value,7)
    I3C_BUS_INIT_NACK_SETDASA 					= makeResultCode(Group.I3C.value,8)
    I3C_BUS_INIT_NACK_SETAASA 					= makeResultCode(Group.I3C.value,9)
    I3C_BUS_INIT_NACK_ENTDAA 					= makeResultCode(Group.I3C.value,10)
    I3C_NACK_ADDRESS 							= makeResultCode(Group.I3C.value,11)
    I3C_I2C_NACK_BYTE 							= makeResultCode(Group.I3C.value,12)
    I3C_TRANSFER_ABORTED_BY_CONTROLLER			= makeResultCode(Group.I3C.value,13)
    I3C_TRANSFER_MWL_REACHED 					= makeResultCode(Group.I3C.value,14)
    I3C_TRANSFER_MRL_REACHED 					= makeResultCode(Group.I3C.value,15)
    I3C_TRANSFER_PARITY_ERROR 					= makeResultCode(Group.I3C.value,16)
    IBI_REQUEST_ACCEPTED 						= makeResultCode(Group.I3C.value,17)
    IBI_REQUEST_ACCEPTED_WITH_PAYLOAD			= makeResultCode(Group.I3C.value,18)
    IBI_REQUEST_REJECTED 						= makeResultCode(Group.I3C.value,19)
    HJ_REQUEST_ACCEPTED 						= makeResultCode(Group.I3C.value,20)
    HJ_REQUEST_REJECTED 						= makeResultCode(Group.I3C.value,21)
    REGISTER_ADDRESS_OUT_OF_RANGE               = makeResultCode(Group.I3C.value,22)
    SURPASSED_MEMORY_SIZE                       = makeResultCode(Group.I3C.value,23)

I3C_RESULT_NAMES = {
    **COMMON_RESULT_NAMES,
    **{result.value: result.name for result in I3cResultCodes}
}

# endregion

#================================================================================#
# region COMMON DEFINITIONS
#================================================================================#

I3C_BROADCAST_ADDRESS       = 0x7E

class I3cAddressStatus_t(Enum):
    """
    Represents the status of the addresses on the I3C bus
    """
    ADDRESS_FREE = 0
    ADDRESS_RESERVED = 1
    ADDRESS_ALREADY_ASSIGNED_TO_I2C_DEVICE = 2
    ADDRESS_ALREADY_ASSIGNED_TO_I3C_DEVICE = 3

def addressToDictionary(address_arr_length, addr_array):
        """
        Converts the array holding invalid address information (the pairs (address, reason it is invalid)) to a
        list of dictionaries with keys "address" and "error" for a more understandable data representation
        """
        address_list = []

        if (address_arr_length > 0):
            for i in range(0, address_arr_length, 2):
                address = addr_array[i]
                attribute = addr_array[i + 1]
                address_list.append({"address": f"0x{address:02X}", "error": I3cAddressStatus_t(attribute).name})

        return address_list

class ENEC(Enum):
    ENINT   = 0x01
    ENCR    = 0x02
    ENHJ    = 0x08

class DISEC(Enum):
    DISINT  = 0x01
    DISCR   = 0x02
    DISHJ   = 0x08

class TransferDirection(Enum):
    """
    This enum represent the transfer directions Read and Write.
    """
    WRITE = 0x00
    READ  = 0x01

class TransferMode(Enum):
    """
    This enum represents the possible values to be assigned to the transfer mode bits in the command parameters.
    """
    I3C_SDR     = 0
    I3C_HDR_DDR = 1
    I2C_MODE    = 2

class I3cPushPullTransferRate(Enum):
    """
    This enum represents the possible values to be assigned to the transfer rate bits in the command parameters.
    """
    PUSH_PULL_2_5_MHZ_10_DC         = 0         # 2.5 MHz, 10% duty cycle
    PUSH_PULL_2_5_MHZ_15_DC         = 1         # 2.5 MHz, 15% duty cycle
    PUSH_PULL_2_5_MHZ_20_DC         = 2         # 2.5 MHz, 20% duty cycle
    PUSH_PULL_2_5_MHZ_25_DC         = 3         # 2.5 MHz, 25% duty cycle
    PUSH_PULL_3_125_MHZ_12_5_DC     = 4         # 3.125 MHz, 12.5% duty cycle
    PUSH_PULL_3_125_MHZ_18_75_DC    = 5         # 3.125 MHz, 18.75% duty cycle
    PUSH_PULL_3_125_MHZ_25_DC       = 6         # 3.125 MHz, 25% duty cycle
    PUSH_PULL_3_125_MHZ_31_25_DC    = 7         # 3.125 MHz, 31.25% duty cycle
    PUSH_PULL_5_MHZ_20_DC       = 8         # 5 MHz, 20% duty cycle
    PUSH_PULL_5_MHZ_30_DC       = 9         # 5 MHz, 30% duty cycle
    PUSH_PULL_5_MHZ_40_DC       = 10        # 5 MHz, 40% duty cycle
    PUSH_PULL_5_MHZ_50_DC       = 11        # 5 MHz, 50% duty cycle
    PUSH_PULL_6_25_MHZ_25_DC        = 12        # 6.25 MHz, 25% duty cycle
    PUSH_PULL_6_25_MHZ_37_5_DC      = 13        # 6.25 MHz, 37.5% duty cycle
    PUSH_PULL_6_25_MHZ_50_DC        = 14        # 6.25 MHz, 50% duty cycle
    PUSH_PULL_7_5_MHZ_30_DC         = 15        # 7.5 MHz, 30% duty cycle
    PUSH_PULL_7_5_MHZ_45_DC         = 16        # 7.5 MHz, 45% duty cycle
    PUSH_PULL_10_MHZ_40_DC          = 17        # 10 MHz, 40% duty cycle
    PUSH_PULL_12_5_MHZ_50_DC        = 18        # 12.5 MHz, 50% duty cycle

class I3cOpenDrainTransferRate(Enum):
    """
    This enum represents the possible values to be assigned to the transfer rate bits in the command parameters.
    """
    OPEN_DRAIN_100_KHZ 		= 0
    OPEN_DRAIN_400_KHZ 		= 1
    OPEN_DRAIN_1_MHZ 	    = 2
    OPEN_DRAIN_2_MHZ		= 3
    OPEN_DRAIN_4_17_MHZ		= 4

class I2cTransferRate(Enum):
    """
    This enum represents the possible values to be assigned to the transfer rate bits in the command parameters.

    Defined in the USB I3C Device class specification V1.0
    """
    _100KHz     = 0
    _400KHz     = 1
    _1MHz       = 2
    _3_4MHz     = 3
    _5MHz       = 4

class I3cDriveStrength(Enum):
    """
    This enum represents the possible values to be assigned to the drive strength bits in the command parameters.
    """
    STANDARD_MODE   = 0
    FAST_MODE       = 1

class I3cPattern(Enum):
    I3C_TARGET_RESET_PATTERN = 0
    I3C_HDR_EXIT_PATTERN     = 1

class I3cCccType(Enum):
    """
    This enum represents the different CCC types.
    """
    CCC_WITHOUT_DEFINING_BYTE   = 0
    CCC_WITH_DEFINING_BYTE      = 1

class I3cTargetResetDefByte(Enum):
    """
    This enum represents the possible values of the definingByte for RSTACT CCC used to perform a Target Reset.

    Defined in the USB I3C Device class specification V1.0
    """
    NO_RESET                            = 0x00
    RESET_I3C_PERIPHERAL                = 0x01
    RESET_WHOLE_TARGET                  = 0x02
    RESET_DEBUG_NETWORK                 = 0x03
    VIRTUAL_TARGET_DETECT               = 0x04
    RETURN_TIME_RESET_PERIPHERAL        = 0x81
    RETURN_TIME_RESET_WHOLE_TARGET      = 0x82
    RETURN_TIME_DEBUG_NETWORK_RESET     = 0x83
    RETURN_VIRTUAL_TARGET_INDICATION    = 0x84

# endregion

#================================================================================#
# region Bus Characteristics Register (BCR)
#================================================================================#

MIN_I3C_BCR_VALUE = 0
MAX_I3C_BCR_VALUE = 127

class I3cBcrMaxDataSpeedLimitBit_t(Enum):
    """
    Enum that represents the bit BCR[0]. Used to indicate if there is a data speed limit.
    """
    NO_DATA_SPEED_LIMIT  = 0x00
    MAX_DATA_SPEED_LIMIT = 0x01

class I3cBcrIbiCapableBit_t(Enum):
    """
    Enum that represents the bit BCR[1]. Shows if the Supernova is capable of requesting IBIs
    """
    NOT_IBI_CAPABLE   = 0x00
    IBI_CAPABLE       = 0x02

class I3cBcrIbiPayloadBit_t(Enum):
    """
    Enum that represents the bit BCR[2]. Indicates if the Supernova is capable of sending data during IBIs.
    """
    IBI_WITHOUT_PAYLOAD     = 0x00
    IBI_WITH_PAYLOAD        = 0x04

class I3cBcrOfflineCapBit_t(Enum):
    """
    Enum that represents the bit BCR[3]. Specifies whether the Supernova has offline capabilities or not.
    """
    OFFLINE_CAPABLE     = 0x00
    OFFLINE_UNCAPABLE   = 0x08

class I3cBcrVirtualSupportBit_t(Enum):
    """
    Enum that represents the bit BCR[4] to indicate if the Supernova is a virtual target or exposes
    other downstream devices.
    """
    NOT_SUPPORTED   = 0x00
    SUPPORTED       = 0x01

class I3cBcrAdvancedCapabilitiesBit_t(Enum):
    """
    Enum that represents the bit BCR[5], Advanced Capabilities.
    """
    NOT_SUPPORTED   = 0x00
    SUPPORTED       = 0x20

class I3cBcrDeviceRoleBits_t(Enum):
    """
    Enum that represents the bit BCR[6] and BCR[7], to indicate the device role.
    """
    I3C_TARGET                  = 0x00
    I3C_CONTROLLER_CAPABLE      = 0x40
    FIRST_MIPI_RESERVED         = 0x80
    SECOND_MIPI_RESERVED        = 0xC0

# BCR Dictionary. This dictionary contains a description for every BCR bit fields.
BCR = {
    "deviceRole": {
        0 : "I3C Target.",
        1 : "I3C Controller capable.",
        2 : "Reserved for future definition by MIPI Alliance I3C WG.",
        3 : "Reserved for future definition by MIPI Alliance I3C WG."
    },

    "advancedCapabilities": {
        0 : "Does not support optional advanced capabilities.",
        1 : "Supports optional advanced capabilities. Use GETCAPS CCC to determine which ones."
    },

    "virtualTargetSupport": {
        0 : "Is not a Virtual Target and does not expose other downstream Device(s).",
        1 : "Is a Virtual Target, or exposes other downstream Device(s)."
    },

    "offlineCapable": {
        0 : "Device retains the Dynamic Address and will always respond to I3C Bus commands.",
        1 : "Device will not always respond to I3C Bus commands."
    },

    "ibiPayload": {
        0 : "No data bytes follow the accepted IBI.",
        1 : "One data byte (MDB) shall follow the accepted IBI, and additional data bytes may follow."
    },

    "ibiRequestCapable": {
        0 : "Not capable.",
        1 : "Capable."
    },

    "maxDataSpeedLimitation": {
        0 : "No Limitation.",
        1 : "Limitation. Controller shall use the GETMXDS CCC to interrogate the Target for specific limitation."
    }
}

# Bus Characteristics Register (BCR).
class I3cBcrBitFields_t(Structure):
    _pack_ = 1
    _fields_ = [("maxDataSpeedLimitation", c_uint8, 1),
                ("ibiRequestCapable", c_uint8, 1),
                ("ibiPayload", c_uint8, 1),
                ("offlineCapable", c_uint8, 1),
                ("virtualTargetSupport", c_uint8, 1),
                ("advancedCapabilities", c_uint8, 1),
                ("deviceRole", c_uint8, 2)]

class I3cBCR_t(Union):
    _fields_ = [("byte", c_uint8 ),
                ("bits", I3cBcrBitFields_t )]

    def toDictionary(self) -> dict:
        return {
            "value": [f"{self.byte:#010b}", self.byte, f"{self.byte:#04x}"],
            "description": {
                "device_role": BCR["deviceRole"][self.bits.deviceRole],
                "advanced_capabilities": BCR["advancedCapabilities"][self.bits.advancedCapabilities],
                "virtual_target_support": BCR["virtualTargetSupport"][self.bits.virtualTargetSupport],
                "offline_capable": BCR["offlineCapable"][self.bits.offlineCapable],
                "ibi_payload": BCR["ibiPayload"][self.bits.ibiPayload],
                "ibi_request_capable": BCR["ibiRequestCapable"][self.bits.ibiRequestCapable],
                "max_data_speed_limitation": BCR["maxDataSpeedLimitation"][self.bits.maxDataSpeedLimitation],
            }
        }

    def __str__(self) -> str:
        return str(self.toDictionary())

# endregion

#================================================================================#
# region Provisioned-ID (PID)
#================================================================================#

class I3cPidBytes_t(Structure):
    _pack_ = 1
    _fields_ = [("PID_5", c_uint8),
                ("PID_4", c_uint8),
                ("PID_3", c_uint8),
                ("PID_2", c_uint8),
                ("PID_1", c_uint8),
                ("PID_0", c_uint8)]

class I3cPID_t(Union):
    _fields_ = [("data", c_uint8 * sizeof(I3cPidBytes_t)),
                ("bytes", I3cPidBytes_t )]

# endregion

#================================================================================#
# region I3C Target Device Configuration
#================================================================================#

class TargetType(Enum):
    """
    Enum that represents the Target Type feature options.

    If the Target device is an I3C device, this field shall be set to 0h. If the Target
    device is an I2C device, this field shall be set to 1h.
    """
    I3C_DEVICE = 0
    I2C_DEVICE = 1

# Target devices features enums.
class TargetInterruptRequest(Enum):
    """
    Enum that represents the Target Interrupt Request (TIR) feature options.

    This field is configurable. This field controls whether the Active I3C Controller
    will accept or reject interrupts from this Target device. If this bit is set to 0b,
    the Active I3C Controller shall ACCEPT interrupts from this Target device. If this
    bit is set to 1b, Active I3C Controller shall REJECT interrupts from this Target
    device.
    """
    REJECT_IBI = 0
    ACCEPT_IBI = 1

class ControllerRoleRequest(Enum):
    """
    Enum that represents the Controller Role Request (CRR) feature options.

    This field is configurable. This field controls whether the Active I3C Controller
    accepts or rejects the I3C Controller role request. If this bit is set to 0b,
    Active I3C Controller shall ACCEPT the I3C Controller role requests from Secondary
    I3C Controllers. If this bit is set to 1b, Active I3C Controller shall REJECT the
    I3C Controller role requests from Secondary I3C Controllers.
    """
    REJECT_CRR = 0
    ACCEPT_CRR = 1

class IBiTimestamp(Enum):
    """
    Enum that represents the IBI Timestamp (IBIT) feature options.

    This field is configurable. This field enables or disables timestamping of IBIs
    from the Target device. If this bit is set to 0b, Active I3C Controller shall
    not timestamp IBIs from this Target device. If this bit is set to 1b, Active I3C
    Controller shall timestamp IBIs from this Target device.
    """
    DISABLE_IBIT = 0
    ENABLE_IBIT  = 1

class SetdasaConfiguration(Enum):
    DO_NOT_USE_SETDASA = 0
    USE_SETDASA = 1

class SetaasaConfiguration(Enum):
    DO_NOT_USE_SETAASA = 0
    USE_SETAASA = 1

class EntdaaConfiguration(Enum):
    DO_NOT_USE_ENTDAA = 0
    USE_ENTDAA = 1

class PendingReadCapability(Enum):
    """
    Enum that represents the Pending Read Capability feature options.

    This field indicates if the I3C Target device supports IBI pending read capability.
    If this bit is set to 0b, the I3C Device does not support IBI pending read. If this
    bit is set to 1b, the I3C Device supports IBI pending read.
    """
    DISABLE_AUTOMATIC_READ = 0
    ENABLE_AUTOMATIC_READ = 1

class I3cTargetConfigurationFields_t(Structure):
    _pack_ = 1
    _fields_ = [("targetType", c_uint8, 1),
                ("acceptIbiRequest", c_uint8, 1),
                ("acceptControllerRoleRequest", c_uint8, 1),
                ("daaUseSETDASA", c_uint8, 1),
                ("daaUseSETAASA", c_uint8, 1),
                ("daaUseENTDAA", c_uint8, 1),
                ("ibiTimestampEnable", c_uint8, 1),
                ("pendingReadCapability", c_uint8, 1)]

class I3cTargetConfiguration_t(Union):
    _fields_ = [("byte", c_uint8),
                ("fields", I3cTargetConfigurationFields_t)]

    def toDictionary(self):
        return {
            "target_type": TargetType(self.fields.targetType).name,
            "interrupt_request": TargetInterruptRequest(self.fields.acceptIbiRequest).name,
            "controller_role_request": ControllerRoleRequest(self.fields.acceptControllerRoleRequest).name,
            "setdasa": SetdasaConfiguration(self.fields.daaUseSETDASA).name,
            "setaasa": SetaasaConfiguration(self.fields.daaUseSETAASA).name,
            "entdaa": EntdaaConfiguration(self.fields.daaUseENTDAA).name,
            "ibi_timestamp": IBiTimestamp(self.fields.ibiTimestampEnable).name,
            "pending_read_capability": PendingReadCapability(self.fields.pendingReadCapability).name
        }

# endregion

#================================================================================#
# region I3C Target Device Entry
#================================================================================#

class I3cTargetDeviceEntry_t(Structure):
    _pack_ = 1
    _fields_ = [("staticAddress", c_uint8),
                ("dynamicAddress", c_uint8),
                ("pid", I3cPID_t),
                ("bcr", I3cBCR_t),
                ("dcr", c_uint8),
                ("mwl", c_uint16),
                ("mrl", c_uint16),
                ("maxIbiPayloadLength", c_uint8),
                ("configuration", I3cTargetConfiguration_t)]

    def toDictionary(self) -> dict:
        return {
            "static_address": self.staticAddress,
            "dynamic_address": self.dynamicAddress,
            "pid": [i for i in self.pid.data],
            "bcr": self.bcr.byte,
            "dcr": self.dcr,
            "mwl": self.mwl,
            "mrl": self.mrl,
            "max_ibi_payload_length": self.maxIbiPayloadLength,
            "configuration": self.configuration.toDictionary()
        }

    def __str__(self) -> str:
        return str(self.toDictionary())

# endregion

#================================================================================#
# region I3C Target Devices Table
#================================================================================#

I3C_MAX_NUMBER_TARGETS = 11

class I3cTargetDevicesTableFields_t(Structure):
    _pack_ = 1
    _fields_ = [("targetCount", c_uint8),
                ("targetList", I3cTargetDeviceEntry_t * I3C_MAX_NUMBER_TARGETS)]

I3cTargetDevicesTableArray_t = c_uint8 * sizeof(I3cTargetDevicesTableFields_t)

class I3cTargetDevicesTable_t(Union):
    _fields_ = [("data", I3cTargetDevicesTableArray_t),
                ("fields", I3cTargetDevicesTableFields_t)]

# endregion

#================================================================================#
# region I3C CONTROLLER INIT
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cControllerInitRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pushPullFrequency", c_uint8),
                ("i3cOpenDrainFrequency", c_uint8),
                ("i2cOpenDrainFrequency", c_uint8),
                ("driveStrength", c_uint8)]

class I3cControllerInitRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cControllerInitRequestParameters_t)]

I3cControllerInitRequestArray_t = c_uint8 * sizeof(I3cControllerInitRequestFields_t)

class I3cControllerInitRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerInitRequestArray_t ),
                ("fields", I3cControllerInitRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I3cControllerInitResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

I3cControllerInitResponseArray_t = c_uint8 * sizeof(I3cControllerInitResponseFields_t)

class I3cControllerInitResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerInitResponseArray_t),
                ("fields", I3cControllerInitResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cControllerInitResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region I3C CONTROLLER SET PARAMETERS
#================================================================================#

# Request ---------------------------------------------------------------------- #
class I3cControllerSetParametersRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pushPullFrequency", c_uint8),
                ("i3cOpenDrainFrequency", c_uint8),
                ("i2cOpenDrainFrequency", c_uint8),
                ("driveStrength", c_uint8)]

class I3cControllerSetParametersRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cControllerSetParametersRequestParameters_t)]

I3cControllerSetParametersRequestArray_t = c_uint8 * sizeof(I3cControllerSetParametersRequestFields_t)

class I3cControllerSetParametersRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerSetParametersRequestArray_t ),
                ("fields", I3cControllerSetParametersRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I3cControllerSetParametersResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

I3cControllerSetParametersResponseArray_t = c_uint8 * sizeof(I3cControllerSetParametersResponseFields_t)

class I3cControllerSetParametersResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerSetParametersResponseArray_t),
                ("fields", I3cControllerSetParametersResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cControllerSetParametersResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region I3C CONTROLLER INIT BUS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cControllerInitBusRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("numberOfTargets", c_uint8)]

I3cControllerInitBusRequestPayload_t = I3cTargetDeviceEntry_t * I3C_MAX_NUMBER_TARGETS

class I3cControllerInitBusRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cControllerInitBusRequestParameters_t ),
                ("payload", I3cControllerInitBusRequestPayload_t)]

I3cControllerInitBusRequestArray_t = c_uint8 * sizeof(I3cControllerInitBusRequestFields_t)

class I3cControllerInitBusRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerInitBusRequestArray_t),
                ("fields", I3cControllerInitBusRequestFields_t)]

    def toBytes(self) -> bytes:
        """
        Method to return an bytes object representing the command
        serialization.
        """
        length = sizeof(CommandRequestHeader_t) + sizeof(I3cControllerInitBusRequestParameters_t) + (sizeof(I3cTargetDeviceEntry_t) * self.fields.parameters.numberOfTargets)
        return bytes(self.data[:length])

# Response --------------------------------------------------------------------- #

class I3cInvalidAddress(Structure):
    _pack_ = 1
    _fields_ = [("address", c_uint8),
                ("status", c_uint8)]

class I3cControllerInitBusResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("invalidTargetsCounter", c_uint8)]

I3cControllerInitBusResponsePayload_t = I3cInvalidAddress * I3C_MAX_NUMBER_TARGETS

class I3cControllerInitBusResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I3cControllerInitBusResponseParameters_t),
                ("payload", I3cControllerInitBusResponsePayload_t)]

I3cControllerInitBusResponseArray_t = c_uint8 * sizeof(I3cControllerInitBusResponseFields_t)

class I3cControllerInitBusResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerInitBusResponseArray_t),
                ("fields", I3cControllerInitBusResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "invalid_addresses": addressToDictionary(self.fields.parameters.invalidTargetsCounter * sizeof(I3cInvalidAddress), self.fields.payload)
        }

# endregion

#================================================================================#
# region I3C CONTROLLER RESET BUS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cControllerResetBusRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

I3cControllerResetBusRequestArray_t = c_uint8 * sizeof(I3cControllerResetBusRequestFields_t)

class I3cControllerResetBusRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerResetBusRequestArray_t ),
                ("fields", I3cControllerResetBusRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I3cControllerResetBusResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

I3cControllerResetBusResponseArray_t = c_uint8 * sizeof(I3cControllerResetBusResponseFields_t)

class I3cControllerResetBusResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerResetBusResponseArray_t ),
                ("fields", I3cControllerResetBusResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cControllerResetBusResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region I3C CONTROLLER GET TARGET DEVICES TABLE
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cControllerGetTargetDevicesTableRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

I3cControllerGetTargetDevicesTableRequestArray_t = c_uint8 * sizeof(I3cControllerGetTargetDevicesTableRequestFields_t)

class I3cControllerGetTargetDevicesTableRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerGetTargetDevicesTableRequestArray_t ),
                ("fields", I3cControllerGetTargetDevicesTableRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I3cControllerGetTargetDevicesTableResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("table", I3cTargetDevicesTable_t)]

class I3cControllerGetTargetDevicesTableResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I3cControllerGetTargetDevicesTableResponseParameters_t)]

I3cControllerGetTargetDevicesTableResponseArray_t = c_uint8 * sizeof(I3cControllerGetTargetDevicesTableResponseFields_t)

class I3cControllerGetTargetDevicesTableResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerGetTargetDevicesTableResponseArray_t ),
                ("fields", I3cControllerGetTargetDevicesTableResponseFields_t )]

    def fromBytes(self, data):
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self):

        targets = []

        numOfTargets = self.fields.parameters.table.fields.targetCount
        for i in range(numOfTargets):
            target = self.fields.parameters.table.fields.targetList[i]
            targets.append(target.toDictionary())

        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "number_of_targets": numOfTargets,
            "table": targets
        }

# endregion

#================================================================================#
# region I3C CONTROLLER SET TARGET DEVICE CONFIGURATION
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cControllerSetTargetDeviceConfigurationRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("targetAddress", c_uint8),
                ("configuration", I3cTargetConfiguration_t)]

class I3cControllerSetTargetDeviceConfigurationRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cControllerSetTargetDeviceConfigurationRequestParameters_t )]

I3cControllerSetTargetDeviceConfigurationRequestArray_t = c_uint8 * sizeof(I3cControllerSetTargetDeviceConfigurationRequestFields_t)

class I3cControllerSetTargetDeviceConfigurationRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerSetTargetDeviceConfigurationRequestArray_t),
                ("fields", I3cControllerSetTargetDeviceConfigurationRequestFields_t)]

# Response --------------------------------------------------------------------- #

class I3cControllerSetTargetDeviceConfigurationResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

I3cControllerSetTargetDeviceConfigurationResponseArray_t = c_uint8 * sizeof(I3cControllerSetTargetDeviceConfigurationResponseFields_t)

class I3cControllerSetTargetDeviceConfigurationResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerSetTargetDeviceConfigurationResponseArray_t ),
                ("fields", I3cControllerSetTargetDeviceConfigurationResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cControllerSetTargetDeviceConfigurationResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region I3C CONTROLLER PRIVATE TRANSFER
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cControllerPrivateTransferRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("targetAddress", c_uint8),
                ("direction", c_uint8, 1),
                ("mode", c_uint8, 2),
                ("nonStop", c_uint8, 1),
                ("startWith7E", c_uint8, 1),
                ("reserved", c_uint8, 3),
                ("hdrDdrCommand", c_uint8),
                ("registerAddressLength", c_uint8),
                ("registerAddress", c_uint8 * MAX_REGISTER_ADDRESS_LENGTH),
                ("payloadLength", c_uint16)]

I3cControllerPrivateTransferRequestPayload_t = c_uint8 * MAX_I3C_PRIVATE_TRANSFER_LENGTH

class I3cControllerPrivateTransferRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cControllerPrivateTransferRequestParameters_t),
                ("payload", I3cControllerPrivateTransferRequestPayload_t)]

I3cControllerPrivateTransferRequestArray_t = c_uint8 * sizeof(I3cControllerPrivateTransferRequestFields_t)

class I3cControllerPrivateTransferRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerPrivateTransferRequestArray_t),
                ("fields", I3cControllerPrivateTransferRequestFields_t )]

    def toBytes(self) -> bytes:
        """
        Method to return an bytes object representing the command
        serialization.
        """
        length = sizeof(CommandRequestHeader_t) + sizeof(I3cControllerPrivateTransferRequestParameters_t)

        if self.fields.parameters.direction == TransferDirection.WRITE.value:
            length += self.fields.parameters.payloadLength

        return bytes(self.data[:length])

# Response --------------------------------------------------------------------- #

class I3cControllerPrivateTransferResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("targetAddress", c_uint8),
                ("direction", c_uint8),
                ("payloadLength", c_uint16)]

I3cControllerPrivateTransferResponsePayload_t = c_uint8 * MAX_I3C_PRIVATE_TRANSFER_LENGTH

class I3cControllerPrivateTransferResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I3cControllerPrivateTransferResponseParameters_t),
                ("payload", I3cControllerPrivateTransferResponsePayload_t)]

I3cControllerPrivateTransferResponseArray_t = c_uint8 * sizeof(I3cControllerPrivateTransferResponseFields_t)

class I3cControllerPrivateTransferResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerPrivateTransferResponseArray_t ),
                ("fields", I3cControllerPrivateTransferResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:
        response = {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "payload_length": self.fields.parameters.payloadLength,
        }

        if self.fields.parameters.direction == TransferDirection.READ.value:
            response["payload"] = self.fields.payload[:self.fields.parameters.payloadLength]

        return response

# endregion

#================================================================================#
# region I3C CONTROLLER CCC TRANSFER
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cControllerCccTransferRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("targetAddress", c_uint8),
                ("direction", c_uint8, 1),
                ("mode", c_uint8, 2),
                ("nonStop", c_uint8, 1),
                ("type", c_uint8, 1),
                ("reserved", c_uint8, 3),
                ("payloadLength",c_uint8),
                ("ccc", c_uint8),
                ("definingByte", c_uint8)]

I3cControllerCccTransferRequestPayload_t = c_uint8 * MAX_I3C_CCC_TRANSFER_LENGTH

class I3cControllerCccTransferRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cControllerCccTransferRequestParameters_t),
                ("payload", I3cControllerCccTransferRequestPayload_t)]

I3cControllerCccTransferRequestArray_t = c_uint8 * sizeof(I3cControllerCccTransferRequestFields_t)

class I3cControllerCccTransferRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerCccTransferRequestArray_t),
                ("fields", I3cControllerCccTransferRequestFields_t )]

    def toBytes(self) -> bytes:
        """
        Method to return an bytes object representing the command
        serialization.
        """
        length = sizeof(CommandRequestHeader_t) + sizeof(I3cControllerCccTransferRequestParameters_t)

        if self.fields.parameters.direction == TransferDirection.WRITE.value:
            length += self.fields.parameters.payloadLength

        return bytes(self.data[:length])

# Response --------------------------------------------------------------------- #

class I3cControllerCccTransferResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("ccc", c_uint8),
                ("targetAddress", c_uint8),
                ("direction", c_uint8),
                ("payloadLength", c_uint8)]

I3cControllerCccTransferResponsePayload_t = c_uint8 * MAX_I3C_CCC_TRANSFER_LENGTH

class I3cControllerCccTransferResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I3cControllerCccTransferResponseParameters_t),
                ("payload", I3cControllerCccTransferResponsePayload_t)]

I3cControllerCccTransferResponseArray_t = c_uint8 * sizeof(I3cControllerCccTransferResponseFields_t)

class I3cControllerCccTransferResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerCccTransferResponseArray_t),
                ("fields", I3cControllerCccTransferResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:
        response = {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "ccc": CCC(self.fields.parameters.ccc).name,
            "payload_length": self.fields.parameters.payloadLength,
        }

        if (self.fields.header.result in [I3cResultCodes.INVALID_TARGET_ADDRESS.value, I3cResultCodes.REPEATED_TARGET_ADDRESS]) and (self.fields.parameters.ccc in [CCC.D_SETDASA.value, CCC.B_SETAASA.value, CCC.B_ENTDAA.value, CCC.D_SETNEWDA.value]):
            response["invalid_addresses"] = addressToDictionary(self.fields.parameters.payloadLength, self.fields.payload)
        elif self.fields.parameters.direction == TransferDirection.READ.value:
            response["payload"] = self.fields.payload[:self.fields.parameters.payloadLength]

        return response

# endregion

#================================================================================#
# region I3C CONTROLLER TRIGGER PATTERN
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cControllerTriggerPatternRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pattern", c_uint8)]

class I3cControllerTriggerPatternRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cControllerTriggerPatternRequestParameters_t)]

I3cControllerTriggerPatternRequestArray_t = c_uint8 * sizeof(I3cControllerTriggerPatternRequestFields_t)

class I3cControllerTriggerPatternRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cControllerTriggerPatternRequestArray_t),
                ("fields", I3cControllerTriggerPatternRequestFields_t)]

# Response --------------------------------------------------------------------- #

class I3cControllerTriggerPatternResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pattern", c_uint8)]

class I3cControllerTriggerPatternResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I3cControllerTriggerPatternResponseParameters_t)]

I3cControllerTriggerPatternResponseArray_t = c_uint8 * sizeof(I3cControllerTriggerPatternResponseFields_t)

class I3cControllerTriggerPatternResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cControllerTriggerPatternResponseArray_t ),
                ("fields", I3cControllerTriggerPatternResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cControllerTriggerPatternResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "pattern": I3cPattern(self.fields.parameters.pattern).name
        }

# endregion

#================================================================================#
# region I3C CONTROLLER IBI REQUEST NOTIFICATION
#================================================================================#

class I3cControllerIbiRequestNotificationParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("address", c_uint8),
                ("payloadLength", c_uint8)]

I3cControllerIbiRequestNotificationPayload_t = c_uint8 * MAX_I3C_IBI_PAYLOAD_LENGTH

class I3cControllerIbiRequestNotificationFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", NotificationHeader_t),
                ("parameters", I3cControllerIbiRequestNotificationParameters_t),
                ("payload", I3cControllerIbiRequestNotificationPayload_t)]

I3cControllerIbiRequestNotificationArray_t = c_uint8 * sizeof(I3cControllerIbiRequestNotificationFields_t)

class I3cControllerIbiRequestNotification_t(Union):
    _fields_ = [("data", I3cControllerIbiRequestNotificationArray_t),
                ("fields", I3cControllerIbiRequestNotificationFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cControllerIbiRequestNotificationArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        result = {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "target_address": self.fields.parameters.address,
            "payload_length": self.fields.parameters.payloadLength,
        }

        if (self.fields.header.result == I3cResultCodes.IBI_REQUEST_ACCEPTED_WITH_PAYLOAD.value):
            result["payload"] = self.fields.payload[:self.fields.parameters.payloadLength]

        return result

    def __str__(self) -> str:
        return str(self.toDictionary())

# endregion

#================================================================================#
# region I3C CONTROLLER HOT-JOIN REQUEST NOTIFICATION
#================================================================================#

class I3cControllerHotJoinRequestNotificationParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("pid", I3cPID_t),
                ("bcr", I3cBCR_t),
                ("dcr", c_uint8),
                ("dynamicAddress",c_uint8)]

class I3cControllerHotJoinRequestNotificationFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", NotificationHeader_t),
                ("parameters", I3cControllerHotJoinRequestNotificationParameters_t)]

I3cControllerHotJoinRequestNotificationArray_t = c_uint8 * sizeof(I3cControllerHotJoinRequestNotificationFields_t)

class I3cControllerHotJoinRequestNotification_t(Union):
    _fields_ = [("data", I3cControllerHotJoinRequestNotificationArray_t),
                ("fields", I3cControllerHotJoinRequestNotificationFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cControllerHotJoinRequestNotificationArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "pid": [i for i in self.fields.parameters.pid.data],
            "bcr": self.fields.parameters.bcr.byte,
            "dcr": self.fields.parameters.dcr,
            "dynamic_address": self.fields.parameters.dynamicAddress
        }

    def __str__(self) -> str:
        return str(self.toDictionary())

# endregion

#================================================================================#
# region I3C COMMON COMMAND CODE DEFINITIONS
#================================================================================#

class CCC(Enum):
    """
    Enum that identifies all the CCC values.
    """
    B_ENEC      = 0x00
    B_DISEC     = 0x01
    B_ENTAS0    = 0x02
    B_ENTAS1    = 0x03
    B_ENTAS2    = 0x04
    B_ENTAS3    = 0x05
    B_RSTDAA    = 0x06
    B_ENTDAA    = 0x07
    B_DEFTGTS   = 0x08
    B_SETMWL    = 0x09
    B_SETMRL    = 0x0A
    B_ENTTM     = 0x0B
    B_SETBUSCON = 0x0C
    MIPI_RS_0D  = 0x0D  # 0x0D – 0x11 - MIPI Reserved
    MIPI_RS_0E  = 0x0E
    MIPI_RS_0F  = 0x0F
    MIPI_RS_10  = 0x10
    MIPI_RS_11  = 0x11
    B_ENDXFER   = 0x12
    MIPI_RS_13  = 0x13  # 0x13 – 0x1E - MIPI Reserved
    MIPI_RS_14  = 0x14
    MIPI_RS_15  = 0x15
    MIPI_RS_16  = 0x16
    MIPI_RS_17  = 0x17
    MIPI_RS_18  = 0x18
    MIPI_RS_19  = 0x19
    MIPI_RS_1A  = 0x1A
    MIPI_RS_1B  = 0x1B
    MIPI_RS_1C  = 0x1C
    MIPI_RS_1D  = 0x1D
    MIPI_RS_1E  = 0x1E
    RES_1F      = 0x1F  	# 0x1F Reserved
    B_ENTHDR0   = 0x20
    B_ENTHDR1   = 0x21
    B_ENTHDR2   = 0x22
    B_ENTHDR3   = 0x23
    B_ENTHDR4   = 0x24
    B_ENTHDR5   = 0x25
    B_ENTHDR6   = 0x26
    B_ENTHDR7   = 0x27
    B_SETXTIME  = 0x28
    B_SETAASA   = 0x29
    B_RSTACT    = 0x2A
    B_DEFGRPA   = 0x2B
    B_RSTGRPA   = 0x2C
    B_MLANE     = 0x2D
    MIPI_WG_2E  = 0x2E  # 0x2E – 0x48 - MIPI I3C WG Reserved
    MIPI_WG_2F  = 0x2F
    MIPI_WG_30  = 0x30
    MIPI_WG_31  = 0x31
    MIPI_WG_32  = 0x32
    MIPI_WG_33  = 0x33
    MIPI_WG_34  = 0x34
    MIPI_WG_35  = 0x35
    MIPI_WG_36  = 0x36
    MIPI_WG_37  = 0x37
    MIPI_WG_38  = 0x38
    MIPI_WG_39  = 0x39
    MIPI_WG_3A  = 0x3A
    MIPI_WG_3B  = 0x3B
    MIPI_WG_3C  = 0x3C
    MIPI_WG_3D  = 0x3D
    MIPI_WG_3E  = 0x3E
    MIPI_WG_3F  = 0x3F
    MIPI_WG_40  = 0x40
    MIPI_WG_41  = 0x41
    MIPI_WG_42  = 0x42
    MIPI_WG_43  = 0x43
    MIPI_WG_44  = 0x44
    MIPI_WG_45  = 0x45
    MIPI_WG_46  = 0x46
    MIPI_WG_47  = 0x47
    MIPI_WG_48  = 0x48
    MIPI_CAM_49 = 0x49  # 0x49 – 0x4C - MIPI Camera WG Reserved – Broadcast CCCs
    MIPI_CAM_4A = 0x4A
    MIPI_CAM_4B = 0x4B
    MIPI_CAM_4C = 0x4C
    MIPI_RS_4D  = 0x4D  # 0x4D – 0x57 - MIPI Reserved – Broadcast CCCs
    MIPI_RS_4E  = 0x4E
    MIPI_RS_4F  = 0x4F
    MIPI_RS_50  = 0x50
    MIPI_RS_51  = 0x51
    MIPI_RS_52  = 0x52
    MIPI_RS_53  = 0x53
    MIPI_RS_54  = 0x54
    MIPI_RS_55  = 0x55
    MIPI_RS_56  = 0x56
    MIPI_RS_57  = 0x57
    MIPI_DWG_58 = 0x58  # 0x58 – 0x5B - MIPI Debug WG Reserved – Broadcast CCCs
    MIPI_DWG_59 = 0x59
    MIPI_DWG_5A = 0x5A
    MIPI_DWG_5B = 0x5B
    MIPIRIOWG5C = 0x5C  # 0x5C – 0x60 - MIPI RIO WG Reserved – Broadcast CCCs
    MIPIRIOWG5D = 0x5D
    MIPIRIOWG5E = 0x5E
    MIPIRIOWG5F = 0x5F
    MIPIRIOWG60 = 0x60
    B_VENCCC_61 = 0x61  # 0x61 – 0x7F - Vendor / Standards Extension – Broadcast CCCs
    B_VENCCC_62 = 0x62
    B_VENCCC_63 = 0x63
    B_VENCCC_64 = 0x64
    B_VENCCC_65 = 0x65
    B_VENCCC_66 = 0x66
    B_VENCCC_67 = 0x67
    B_VENCCC_68 = 0x68
    B_VENCCC_69 = 0x69
    B_VENCCC_6A = 0x6A
    B_VENCCC_6B = 0x6B
    B_VENCCC_6C = 0x6C
    B_VENCCC_6D = 0x6D
    B_VENCCC_6E = 0x6E
    B_VENCCC_6F = 0x6F
    B_VENCCC_70 = 0x70
    B_VENCCC_71 = 0x71
    B_VENCCC_72 = 0x72
    B_VENCCC_73 = 0x73
    B_VENCCC_74 = 0x74
    B_VENCCC_75 = 0x75
    B_VENCCC_76 = 0x76
    B_VENCCC_77 = 0x77
    B_VENCCC_78 = 0x78
    B_VENCCC_79 = 0x79
    B_VENCCC_7A = 0x7A
    B_VENCCC_7B = 0x7B
    B_VENCCC_7C = 0x7C
    B_VENCCC_7D = 0x7D
    B_VENCCC_7E = 0x7E
    B_VENCCC_7F = 0x7F
    D_ENEC      = 0x80  # DIRECT CCCs
    D_DISEC     = 0x81
    D_ENTAS0    = 0x82
    D_ENTAS1    = 0x83
    D_ENTAS2    = 0x84
    D_ENTAS3    = 0x85
    D_RSTDAA    = 0x86  # 0x86 - DEPRECATED: RSTDAA Direct. Reset Dynamic Address Assignment
    D_SETDASA   = 0x87
    D_SETNEWDA  = 0x88
    D_SETMWL    = 0x89
    D_SETMRL    = 0x8A
    D_GETMWL    = 0x8B
    D_GETMRL    = 0x8C
    D_GETPID    = 0x8D
    D_GETBCR    = 0x8E
    D_GETDCR    = 0x8F
    D_GETSTATUS = 0x90
    D_GETACCCR  = 0x91
    D_ENDXFER   = 0x92
    D_SETBRGTGT = 0x93
    D_GETMXDS   = 0x94
    D_GETCAPS   = 0x95
    D_SETROUTE  = 0x96
    D_D2DXFER   = 0x97
    D_SETXTIME  = 0x98
    D_GETXTIME  = 0x99
    D_RSTACT    = 0x9A
    D_SETGRPA   = 0x9B
    D_RSTGRPA   = 0x9C
    D_MLANE     = 0x9D
    MIPI_WG_9E  = 0x9E  # 0x9E – 0xBF - MIPI I3C WG Reserved – Direct CCCs
    MIPI_WG_9F  = 0x9F
    MIPI_WG_A0  = 0xA0
    MIPI_WG_A1  = 0xA1
    MIPI_WG_A2  = 0xA2
    MIPI_WG_A3  = 0xA3
    MIPI_WG_A4  = 0xA4
    MIPI_WG_A5  = 0xA5
    MIPI_WG_A6  = 0xA6
    MIPI_WG_A7  = 0xA7
    MIPI_WG_A8  = 0xA8
    MIPI_WG_A9  = 0xA9
    MIPI_WG_AA  = 0xAA
    MIPI_WG_AB  = 0xAB
    MIPI_WG_AC  = 0xAC
    MIPI_WG_AD  = 0xAD
    MIPI_WG_AE  = 0xAE
    MIPI_WG_AF  = 0xAF
    MIPI_WG_B0  = 0xB0
    MIPI_WG_B1  = 0xB1
    MIPI_WG_B2  = 0xB2
    MIPI_WG_B3  = 0xB3
    MIPI_WG_B4  = 0xB4
    MIPI_WG_B5  = 0xB5
    MIPI_WG_B6  = 0xB6
    MIPI_WG_B7  = 0xB7
    MIPI_WG_B8  = 0xB8
    MIPI_WG_B9  = 0xB9
    MIPI_WG_BA  = 0xBA
    MIPI_WG_BB  = 0xBB
    MIPI_WG_BC  = 0xBC
    MIPI_WG_BD  = 0xBD
    MIPI_WG_BE  = 0xBE
    MIPI_WG_BF  = 0xBF
    MIPI_CAM_C0 = 0xC0  # 0xC0 – 0xC3 - MIPI Camera WG Reserved – Direct CCCs
    MIPI_CAM_C1 = 0xC1
    MIPI_CAM_C2 = 0xC2
    MIPI_CAM_C3 = 0xC3
    MIPI_RS_C4  = 0xC4  # 0xC4 – 0xD6 - MIPI Reserved – Direct CCCs
    MIPI_RS_C5  = 0xC5
    MIPI_RS_C6  = 0xC6
    MIPI_RS_C7  = 0xC7
    MIPI_RS_C8  = 0xC8
    MIPI_RS_C9  = 0xC9
    MIPI_RS_CA  = 0xCA
    MIPI_RS_CB  = 0xCB
    MIPI_RS_CC  = 0xCC
    MIPI_RS_CD  = 0xCD
    MIPI_RS_CE  = 0xCE
    MIPI_RS_CF  = 0xCF
    MIPI_RS_D0  = 0xD0
    MIPI_RS_D1  = 0xD1
    MIPI_RS_D2  = 0xD2
    MIPI_RS_D3  = 0xD3
    MIPI_RS_D4  = 0xD4
    MIPI_RS_D5  = 0xD5
    MIPI_RS_D6  = 0xD6
    MIPI_DWG_D7 = 0xD7  # 0xD7 – 0xDA - MIPI Debug WG Reserved – Direct CCCs
    MIPI_DWG_D8 = 0xD8
    MIPI_DWG_D9 = 0xD9
    MIPI_DWG_DA = 0xDA
    MIPIRIOWGDB = 0xDB  # 0xDB – 0xDF - MIPI RIO WG Reserved – Direct CCCs
    MIPIRIOWGDC = 0xDC
    MIPIRIOWGDD = 0xDD
    MIPIRIOWGDE = 0xDE
    MIPIRIOWGDF = 0xDF
    D_VENCCC_E0 = 0xE0  # 0xE0 – 0xFE - Vendor / Standards Extension – Direct CCCs
    D_VENCCC_E1 = 0xE1
    D_VENCCC_E2 = 0xE2
    D_VENCCC_E3 = 0xE3
    D_VENCCC_E4 = 0xE4
    D_VENCCC_E5 = 0xE5
    D_VENCCC_E6 = 0xE6
    D_VENCCC_E7 = 0xE7
    D_VENCCC_E8 = 0xE8
    D_VENCCC_E9 = 0xE9
    D_VENCCC_EA = 0xEA
    D_VENCCC_EB = 0xEB
    D_VENCCC_EC = 0xEC
    D_VENCCC_ED = 0xED
    D_VENCCC_EE = 0xEE
    D_VENCCC_EF = 0xEF
    D_VENCCC_F0 = 0xF0
    D_VENCCC_F1 = 0xF1
    D_VENCCC_F2 = 0xF2
    D_VENCCC_F3 = 0xF3
    D_VENCCC_F4 = 0xF4
    D_VENCCC_F5 = 0xF5
    D_VENCCC_F6 = 0xF6
    D_VENCCC_F7 = 0xF7
    D_VENCCC_F8 = 0xF8
    D_VENCCC_F9 = 0xF9
    D_VENCCC_FA = 0xFA
    D_VENCCC_FB = 0xFB
    D_VENCCC_FC = 0xFC
    D_VENCCC_FD = 0xFD
    D_VENCCC_FE = 0xFE
    MIPI_WG_FF  = 0xFF  # 0xFF - MIPI I3C WG Reserved

# endregion

#================================================================================#
# region I3C TARGET MODE - GENERAL DEFINITIONS
#================================================================================#

I3C_TARGET_MEMORY_SIZE = 1024
I3C_TARGET_MAX_MWL = 1024
I3C_TARGET_MAX_MRL = 1024

class I3cTargetMemoryLayout_t(Enum):
    """
    Different memory layouts the Supernova as an I3C target can represent
    """
    MEMORY_1_BYTE_X_1024_REGS = 0x00
    MEMORY_2_BYTES_X_512_REGS = 0x01
    MEMORY_4_BYTES_X_256_REGS = 0x02

class I3cTargetDcr_t(Enum):
    I3C_SECONDARY_CONTROLLER    = 0xC4
    I3C_TARGET_MEMORY           = 0xC5
    I3C_TARGET_MICROCONTROLLER  = 0xC6

class I3cTargetBusEvent_t(Enum):
    """
    This enum represents the type of event when the Supernova acts an I3C target.
    """
    I3C_WRITE_TRANSFER_EVENT            = 0
    I3C_READ_TRANSFER_EVENT             = 1
    I3C_CCC_TRANSFER_EVENT              = 2
    I3C_TARGET_DYN_ADDR_CHANGE_EVENT    = 3

# endregion

#================================================================================#
# region I3C TARGET INIT
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cTargetInitRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("memoryLayout", c_uint8),
                ("partNo", c_uint32),
                ("randomValueFlag", c_uint8),
                ("vendorId", c_uint16),
                ("bcr", I3cBCR_t),
                ("dcr", c_uint8),
                ("staticAddress", c_uint8),
                ("mwl", c_uint16),
                ("mrl", c_uint16)]

class I3cTargetInitRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cTargetInitRequestParameters_t)]

I3cTargetInitRequestArray_t = c_uint8 * sizeof(I3cTargetInitRequestFields_t)

class I3cTargetInitRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cTargetInitRequestArray_t ),
                ("fields", I3cTargetInitRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I3cTargetInitResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

I3cTargetInitResponseArray_t = c_uint8 * sizeof(I3cTargetInitResponseFields_t)

class I3cTargetInitResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cTargetInitResponseArray_t),
                ("fields", I3cTargetInitResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cTargetInitResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region I3C TARGET SET PARAMETERS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cTargetSetParametersRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("memoryLayout", c_uint8),
                ("partNo", c_uint32),
                ("randomValueFlag", c_uint8),
                ("vendorId", c_uint16),
                ("bcr", I3cBCR_t),
                ("dcr", c_uint8),
                ("staticAddress", c_uint8),
                ("mwl", c_uint16),
                ("mrl", c_uint16)]

class I3cTargetSetParametersRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cTargetSetParametersRequestParameters_t)]

I3cTargetSetParametersRequestArray_t = c_uint8 * sizeof(I3cTargetSetParametersRequestFields_t)

class I3cTargetSetParametersRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cTargetSetParametersRequestArray_t ),
                ("fields", I3cTargetSetParametersRequestFields_t )]

# Response --------------------------------------------------------------------- #

class I3cTargetSetParametersResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

I3cTargetSetParametersResponseArray_t = c_uint8 * sizeof(I3cTargetSetParametersResponseFields_t)

class I3cTargetSetParametersResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cTargetSetParametersResponseArray_t),
                ("fields", I3cTargetSetParametersResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = I3cTargetSetParametersResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result]
        }

#endregion

#================================================================================#
# region I3C TARGET TRANSFER MEMORY
#================================================================================#

# Request ---------------------------------------------------------------------- #

class I3cTargetTransferMemoryRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("memoryAddress", c_uint16),
                ("payloadLength", c_uint16)]

I3cTargetTransferMemoryRequestPayload_t = c_uint8 * I3C_TARGET_MEMORY_SIZE

class I3cTargetTransferMemoryRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", I3cTargetTransferMemoryRequestParameters_t),
                ("payload", I3cTargetTransferMemoryRequestPayload_t)]

I3cTargetTransferMemoryRequestArray_t = c_uint8 * sizeof(I3cTargetTransferMemoryRequestFields_t)

class I3cTargetTransferMemoryRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", I3cTargetTransferMemoryRequestArray_t),
                ("fields", I3cTargetTransferMemoryRequestFields_t)]

    def toBytes(self) -> bytes:
        """
        Method to return an bytes object representing the command serialization.
        """
        length = sizeof(CommandRequestHeader_t) + sizeof(I3cTargetTransferMemoryRequestParameters_t)

        if self.fields.header.code == I3cCommandCodes.I3C_TARGET_WRITE_MEMORY.value:
            length += self.fields.parameters.payloadLength

        return bytes(self.data[:length])

# Response --------------------------------------------------------------------- #

class I3cTargetTransferMemoryResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("payloadLength", c_uint16)]

I3cTargetTransferMemoryResponsePayload_t = c_uint8 * I3C_TARGET_MEMORY_SIZE

class I3cTargetTransferMemoryResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", I3cTargetTransferMemoryResponseParameters_t),
                ("payload", I3cTargetTransferMemoryResponsePayload_t)]

I3cTargetTransferMemoryResponseArray_t = c_uint8 * sizeof(I3cTargetTransferMemoryResponseFields_t)

class I3cTargetTransferMemoryResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", I3cTargetTransferMemoryResponseArray_t),
                ("fields", I3cTargetTransferMemoryResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:
        d = {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "payload_length": self.fields.parameters.payloadLength
        }

        if (self.fields.header.code == I3cCommandCodes.I3C_TARGET_READ_MEMORY.value):
            d["payload"] = self.fields.payload[:self.fields.parameters.payloadLength]

        return d

# endregion

#================================================================================#
# region I3C TARGET NOTIFICATION
#================================================================================#

class I3cTargetBusEventNotificationParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("event", c_uint8),
                ("targetAddress", c_uint8),
                ("memoryAddress", c_uint16),
                ("payloadLength", c_uint16)]

I3cTargetBusEventNotificationPayload_t = c_uint8 * I3C_TARGET_MEMORY_SIZE

class I3cTargetBusEventNotificationFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", NotificationHeader_t),
                ("parameters", I3cTargetBusEventNotificationParameters_t),
                ("payload", I3cTargetBusEventNotificationPayload_t)]

I3cTargetBusEventNotificationArray_t = c_uint8 * sizeof(I3cTargetBusEventNotificationFields_t)

class I3cTargetBusEventNotification_t(Union):
    _fields_ = [("data", I3cTargetBusEventNotificationArray_t ),
                ("fields", I3cTargetBusEventNotificationFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:
        d = {
            "id": self.fields.header.id,
            "command": I3C_COMMAND_NAMES[self.fields.header.code],
            "result": I3C_RESULT_NAMES[self.fields.header.result],
            "event": I3cTargetBusEvent_t(self.fields.parameters.event).name,
        }

        if (self.fields.parameters.event == I3cTargetBusEvent_t.I3C_WRITE_TRANSFER_EVENT.value) or (self.fields.parameters.event == I3cTargetBusEvent_t.I3C_READ_TRANSFER_EVENT.value):
            d["target_address"] = self.fields.parameters.targetAddress
            d["memory_address"] = self.fields.parameters.memoryAddress
            d["payload_length"] = self.fields.parameters.payloadLength
            d["payload"] = self.fields.payload[:self.fields.parameters.payloadLength]

        elif (self.fields.parameters.event == I3cTargetBusEvent_t.I3C_CCC_TRANSFER_EVENT.value):
            d["target_address"] = self.fields.parameters.targetAddress

        elif (self.fields.parameters.event == I3cTargetBusEvent_t.I3C_TARGET_DYN_ADDR_CHANGE_EVENT.value):
            d["new_address"] = self.fields.parameters.targetAddress

        return d

    def __str__(self) -> str:
        return str(self.toDictionary())

# endregion
