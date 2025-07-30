from .serializers import *
from ..helpers.validator import check_type, check_range, check_valid_id, check_byte_array, getRepeatedItems
from ...utils.system_message import SystemMessage, SystemModules, RequestValidatorOpcode

#================================================================================#
# region Helper functions
#================================================================================#

def validateI3cControllerConfiguration(metadata: dict, result: SystemMessage):
    """
    This function validates the metadata for the commands that configure the I3C controller.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        SystemMessage to be updated.

    """

    notValidFrequenciesPair = [ (I3cPushPullTransferRate.PUSH_PULL_2_5_MHZ_10_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_2_5_MHZ_15_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_2_5_MHZ_20_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_2_5_MHZ_25_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_2_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_2_5_MHZ_25_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_3_125_MHZ_12_5_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_3_125_MHZ_18_75_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_3_125_MHZ_25_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_3_125_MHZ_31_25_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_2_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_3_125_MHZ_31_25_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_5_MHZ_40_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_5_MHZ_50_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_2_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_5_MHZ_50_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ),
                                (I3cPushPullTransferRate.PUSH_PULL_6_25_MHZ_50_DC, I3cOpenDrainTransferRate.OPEN_DRAIN_4_17_MHZ) ]

    if (not check_type(metadata["pushPullRate"], I3cPushPullTransferRate)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pushPullRate value"
    if (not check_type(metadata["i3cOpenDrainRate"], I3cOpenDrainTransferRate)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for i3cOpenDrainRate value"
    if (not check_type(metadata["i2cOpenDrainRate"], I2cTransferRate)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for i2cOpenDrainRate value"
    if (not check_type(metadata["driveStrength"], I3cDriveStrength)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for driveStrength value"
    if (metadata["pushPullRate"], metadata["i3cOpenDrainRate"]) in notValidFrequenciesPair:
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: invalid frequency pair"

def validateI3cControllerTransfer(metadata: dict, result: SystemMessage, isWrite: bool):
    """
    This function validates the metadata for the commands that perform I3C controller transfers.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        SystemMessage to be updated.
    isWrite : bool
        Flag to indicate if the transfer is a write operation.

    """
    if (not check_type(metadata["mode"], TransferMode)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for mode value"
    if (not check_type(metadata["registerAddress"], list)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for registerAddress value"
    if (not check_byte_array(metadata["registerAddress"],MAX_REGISTER_ADDRESS_LENGTH)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: registerAddress array length out of range or wrong type"
    if isWrite:
        if (not check_type(metadata["data"], list)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: wrong type for data value"
        if (not check_byte_array(metadata["data"],MAX_I3C_PRIVATE_TRANSFER_LENGTH)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: data array length out of range or wrong type"
    else:
        if (not check_range(metadata["length"], int, 1, MAX_I3C_PRIVATE_TRANSFER_LENGTH)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: length value out of range"

def validateI3cControllerHdrDdrTransfer(metadata: dict, result: SystemMessage, isWrite: bool):
    """
    This function validates the metadata for the commands that perform I3C controller
    write transfer in HDR-DDR mode.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        SystemMessage to be updated.
    isWrite : bool
        Flag to indicate if the transfer is a write operation.

    """
    if isWrite:
        if (not check_type(metadata["data"], list)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: wrong type for data value"
        if (not check_byte_array(metadata["data"],MAX_I3C_PRIVATE_TRANSFER_LENGTH)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: data array length out of range or wrong type"
        # Check if the length is even
        if (len(metadata["data"]) % 2 != 0 or not check_byte_array(metadata["data"],MAX_I3C_PRIVATE_TRANSFER_LENGTH)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: data array length must be even in the range [2, 1024]"
        # Check that the HDR-DDR Write command is in the range 8'h00 to 8'h7F
        if (not check_range(metadata["command"], int, 0x00, 0x7F)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: the HDR-DDR command in write transfers must be in the range [0x00, 0x7F]"
    else:
        # Check if the length is even
        if (metadata["length"] % 2 != 0 or not check_range(metadata["length"], int, 2, MAX_I3C_PRIVATE_TRANSFER_LENGTH) ):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: data length must be even and in the range [2, 1024]"
        # Check that the HDR-DDR Read command is in the range 8'h80 to 8'hFF
        if (not check_range(metadata["command"], int, 0x80, 0xFF)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: the HDR-DDR command in read transfers must be in the range [0x80, 0xFF]"

def validateI3cTargetConfiguration(metadata: dict, result: SystemMessage):
    """
    This function validates the metadata for the commands that configure the I3C target.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        SystemMessage to be updated.

    """
    if (not check_type(metadata["memoryLayout"], I3cTargetMemoryLayout_t)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for memory layout value"
    if (not check_type(metadata["pid"], list)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for PID value"
    if (not check_byte_array(metadata["pid"], sizeof(I3cPidBytes_t))):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: PID length should be 6 bytes"
    if (not check_range(metadata["bcr"], int, MIN_I3C_BCR_VALUE, MAX_I3C_BCR_VALUE)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = f"ARGUMENT ERROR: BCR out of range [{MIN_I3C_BCR_VALUE},{MAX_I3C_BCR_VALUE}]"
    if (not check_type(metadata["dcr"], I3cTargetDcr_t)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for DCR value"
    if (not check_range(metadata["staticAddress"], int, 0, 127)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: Static Address out of range [0,127]"

    i2c_reserved_addresses = list(range(0x00, 0x08)) + list(range(0x78, 0x80))

    if (metadata["staticAddress"] in i2c_reserved_addresses):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: Invalid Static Address value. Reserved by I2C protocol"

    if (not check_range(metadata["mwl"], int, 0, I3C_TARGET_MAX_MWL)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = f"ARGUMENT ERROR: Maximum Write Length out of range [0,{I3C_TARGET_MAX_MWL}]"
    if (not check_range(metadata["mrl"], int, 0, I3C_TARGET_MAX_MRL)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = f"ARGUMENT ERROR: Maximum Read Length out of range [0,{I3C_TARGET_MAX_MRL}]"

def validateI3cTargetTransfer(metadata: dict, result: SystemMessage, isWrite: bool):
    """
    This function validates the metadata for the commands that perform I3C Target transfers.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        SystemMessage to be updated.
    isWrite : bool
        Flag to indicate if the transfer is a write operation.

    """
    if (not check_range(metadata["memoryAddress"],int,0,I3C_TARGET_MEMORY_SIZE)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: Invalid memory address value"
    if isWrite:
        if (not check_type(metadata["data"], list)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: wrong type for data value"
        if (len(metadata["data"]) == 0):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: no data input"
        if (not check_byte_array(metadata["data"],I3C_TARGET_MEMORY_SIZE)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: invalid data input"
    else:
        if (not check_range(metadata["length"],int,0,I3C_TARGET_MEMORY_SIZE)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: invalid length value"

# endregion

#================================================================================#
# region I3C CONTROLLER INIT validator
#================================================================================#

def i3cControllerInitValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER INIT command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER INIT request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    
    validateI3cControllerConfiguration(metadata, result)
    

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerInitSerializer(metadata["id"], metadata["pushPullRate"], metadata["i3cOpenDrainRate"], metadata["i2cOpenDrainRate"], metadata["driveStrength"])

    return request, response, result

#endregion

#================================================================================#
# region I3C CONTROLLER SET PARAMETERS validator
#================================================================================#

def i3cControllerSetParametersValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER SET PARAMETERS command to perform an I3C Private Read Transfer.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER SET PARAMETERS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    
    validateI3cControllerConfiguration(metadata, result)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerSetParametersSerializer(metadata["id"], metadata["pushPullRate"], metadata["i3cOpenDrainRate"], metadata["i2cOpenDrainRate"], metadata["driveStrength"])

    return request, response, result

#endregion

#================================================================================#
# region I3C CONTROLLER INIT BUS validator
#================================================================================#

def i3cControllerInitBusValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER INIT BUS command.
    Validates the targetDeviceTable of the user request. Checks that all I3C devices have a DAA method assigned and that there
    are no repeated addresses:
    - static address for I2C targets and I3C targets to be initialized with SETAASA
    - static and dynamic addresses for I3C targets to be initialized with SETDASA
    - dynamic addresses for I3C targets to be initialized with ENTDAA

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """

    request = None
    response = None

    def verifyI3cDynamicAddressAssignmentMethod(targetDeviceTable: dict):
        """
        Verifies that all I3C entries from the targetDeviceTable have a DAA method assigned.

        Arguments
        ---------
        dict: dictionary of metadata that represents the targetDeviceTable for I3cInitBusRequest_t

        Returns
        -------
        indexOfAddrWithoutMethod
            Index of the entries from targetDeviceTable that does not indicate a DAA method.

        """

        indexOfAddrWithoutMethod = []
        for index, target in targetDeviceTable.items():
            if ((target["configuration"]["targetType"] == TargetType.I3C_DEVICE) and
                ( target["configuration"]["daaUseSETDASA"] == False) and ( target["configuration"]["daaUseSETAASA"] == False) and ( target["configuration"]["daaUseENTDAA"] == False)):
                indexOfAddrWithoutMethod.append(index)
        return indexOfAddrWithoutMethod

    def getRepeatedAddresses(targetDeviceTable: dict):
        """
        Gets all the repeated addresses from the targetDeviceTable argument.

        Arguments
        ---------
        dict: dictionary of metadata that represents the targetDeviceTable for I3cInitBusRequest_t

        Returns
        -------
        listOfAddresses
           List of Addresses repeated in targetDeviceTable.

        """

        # Address used for SETDASA point to point
        SETDASA_POINT_TO_POINT_ADDR = 0x01

        listOfAddresses = []

        for target in targetDeviceTable.values():
            if (target["configuration"]["targetType"] == TargetType.I3C_DEVICE):

                # If the I3C device supports SETDASA and its static and dynamic addresses are SETDASA_POINT_TO_POINT_ADDR it might refer to a point-to-point SETDASA
                if not((target["configuration"]["daaUseSETDASA"] == True) and (target['staticAddress'] == SETDASA_POINT_TO_POINT_ADDR) and (target['dynamicAddress'] == SETDASA_POINT_TO_POINT_ADDR)):

                    if (target["configuration"]["daaUseSETDASA"] == True) or (target["configuration"]["daaUseENTDAA"] == True):
                        listOfAddresses.append(target['dynamicAddress'])

                    if (target["configuration"]["daaUseSETDASA"] == True) or (target["configuration"]["daaUseSETAASA"] == True):
                        listOfAddresses.append(target['staticAddress'])

            if (target["configuration"]["targetType"] == TargetType.I2C_DEVICE):
                listOfAddresses.append(target['staticAddress'])

        # Return the list of repeated addresses
        return getRepeatedItems(listOfAddresses)

    if metadata.get("targetDeviceTable") is not None:
        targetDeviceTable = metadata["targetDeviceTable"]

        listOfTargetsWithoutDaaMethod = verifyI3cDynamicAddressAssignmentMethod(targetDeviceTable)
        if listOfTargetsWithoutDaaMethod:
            targets_str = ', '.join([f"{target_index}" for target_index in listOfTargetsWithoutDaaMethod])
            message = f"I3C CONTROLLER INIT BUS failed: target/s in position {targets_str} of the input table not supporting any DAA method"
            result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, message)
            return request, response, result

        listOfRepeatedAddr = getRepeatedAddresses(targetDeviceTable)
        if listOfRepeatedAddr:
            addresses_str = ', '.join([f"0x{addr:02X}" for addr in listOfRepeatedAddr])
            message = f"I3C CONTROLLER INIT BUS failed: address/es {addresses_str} repeated"
            result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.FAIL, message)
            return request, response, result

    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER INIT BUS request success")

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerInitBusSerializer(metadata["id"], metadata["targetDeviceTable"])

    return request, response, result

#endregion

#================================================================================#
# region I3C CONTROLLER RESET BUS validator
#================================================================================#

def i3cControllerResetBusValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER RESET BUS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER RESET BUS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerResetBusSerializer(metadata["id"])

    return request, response, result

#endregion

#================================================================================#
# region I3C CONTROLLER GET TARGET DEVICES TABLE validator
#================================================================================#

def i3cControllerGetTargetDevicesTableValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER GET TARGET DEVICES TABLE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER GET TARGET DEVICES TABLE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerGetTargetDevicesTableSerializer(metadata["id"])

    return request, response, result

#endregion

#================================================================================#
# region I3C CONTROLLER SET TARGET DEVICE CONFIGURATION validator
#================================================================================#

def i3cControllerSetTargetDeviceConfigurationValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER SET TARGET DEVICE CONFIGURATION command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C SET TARGET DEVICE CONFIG request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerSetTargetDeviceConfigurationSerializer(metadata["id"], metadata["targetAddress"], metadata["configuration"])

    return request, response, result

#endregion

#================================================================================#
# region I3C CONTROLLER PRIVATE WRITE validator
#================================================================================#

def i3cControllerWriteValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER PRIVATE TRANSFER command to perform an I3C Private Write Transfer.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER PRIVATE WRITE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    validateI3cControllerTransfer(metadata, result, isWrite=True)
    
    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerWriteSerializer(metadata["id"], metadata["targetAddress"], metadata["mode"], metadata["registerAddress"], metadata["data"], metadata["startWith7E"])

    return request, response, result

def i3cControllerHdrDdrWriteValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER PRIVATE TRANSFER command to perform an I3C Private Write Transfer in HDR-DDR mode.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER PRIVATE WRITE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    validateI3cControllerHdrDdrTransfer(metadata, result, isWrite=True)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerHdrDdrWriteSerializer(metadata["id"], metadata["targetAddress"], metadata["command"], metadata["data"])

    return request, response, result

#endregion

#================================================================================#
# region I3C CONTROLLER PRIVATE READ validator
#================================================================================#

def i3cControllerReadValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER PRIVATE TRANSFER command to perform an I3C Private Read Transfer.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER PRIVATE READ request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    
    validateI3cControllerTransfer(metadata, result, isWrite=False)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerReadSerializer(metadata["id"], metadata["targetAddress"], metadata["mode"], metadata["registerAddress"], metadata["length"], metadata["startWith7E"])

    return request, response, result

def i3cControllerHdrDdrReadValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER PRIVATE TRANSFER command to perform an I3C Private Read Transfer in HDR-DDR mode.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER PRIVATE READ request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    validateI3cControllerHdrDdrTransfer(metadata, result, isWrite=False)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerHdrDdrReadSerializer(metadata["id"], metadata["targetAddress"], metadata["command"], metadata["length"])

    return request, response, result


#endregion

#================================================================================#
# region I3C CONTROLLER CCC TRANSFER validator
#================================================================================#

def i3cControllerCccTransferValidator(metadata: dict):
    """
    This function validates the metadata for the I3C CONTROLLER CCC TRANSFER command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C SEND CCC request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["mode"], TransferMode)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for mode value"
    if (not check_type(metadata["direction"], TransferDirection)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for direction value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerCccTransferSerializer(metadata["id"], metadata["targetAddress"], metadata["direction"], metadata["mode"], metadata["commandType"], metadata["defByte"], metadata["ccc"], metadata["length"], metadata["data"])

    return request, response, result

#endregion

#================================================================================#
# region I3C CONTROLLER TRIGGER PATTERN validator
#================================================================================#

def i3cControllerTriggerPatternValidator(metadata: dict):
    """
    This function validates the metadata for the I3C TRIGGER PATTERN command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C CONTROLLER TRIGGER PATTERN request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["pattern"], I3cPattern)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pattern value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cControllerTriggerPatternSerializer(metadata["id"],  metadata["pattern"])

    return request, response, result

#endregion

#================================================================================#
# region I3C TARGET validators
#================================================================================#

def i3cTargetInitValidator(metadata: dict):
    """
    This function validates the metadata for the I3C TARGET INIT command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET INIT request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    
    validateI3cTargetConfiguration(metadata, result)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cTargetInitSerializer(metadata["id"], metadata["memoryLayout"], metadata["pid"], metadata["bcr"], metadata["dcr"], metadata["staticAddress"], metadata["mwl"], metadata["mrl"])

    return request, response, result

def i3cTargetSetParametersValidator(metadata: dict):
    """
    This function validates the metadata for the I3C TARGET SET PARAMETERS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET SET PARAMETERS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    validateI3cTargetConfiguration(metadata, result)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cTargetSetParametersSerializer(metadata["id"], metadata["memoryLayout"], metadata["pid"], metadata["bcr"], metadata["dcr"], metadata["staticAddress"], metadata["mwl"], metadata["mrl"])

    return request, response, result

def i3cTargetWriteMemoryValidator(metadata: dict):
    """
    This function validates the metadata for the I3C TARGET WRITE MEMORY command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET WRITE MEMORY request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "I3C TARGET WRITE MEMORY request failed, wrong id value"
    
    validateI3cTargetTransfer(metadata, result, isWrite=True)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cTargetWriteMemorySerializer(metadata["id"], metadata["memoryAddress"], metadata["data"])

    return request, response, result

def i3cTargetReadMemoryValidator(metadata: dict):
    """
    This function validates the metadata for the I3C TARGET READ MEMORY command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I3C TARGET READ MEMORY request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "I3C TARGET READ MEMORY request failed, wrong id value"

    validateI3cTargetTransfer(metadata, result, isWrite=False)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i3cTargetReadMemorySerializer(metadata["id"], metadata["memoryAddress"], metadata["length"])

    return request, response, result

#endregion