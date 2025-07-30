from .serializers import *
from ..helpers.validator import check_type, check_valid_id, check_range, check_byte_array
from ...utils.system_message import SystemMessage, SystemModules, RequestValidatorOpcode

#===============================================================================
# region Helper functions
#===============================================================================

def validateI2cControllerConfiguration(metadata: dict, result: SystemMessage):
    """
    This function validates the metadata for the commands that configure the I2C controller.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        System message to be updated.

    """
    if (not check_range(metadata["frequency_Hz"], int, I2C_CONTROLLER_MIN_FREQUENCY, I2C_CONTROLLER_MAX_FREQUENCY)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: frequency value out of range (100 kHz - 1 MHz)"
    if (not check_type(metadata["pullUpValue"], I2cPullUpResistorsValue)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pull up resistors value"

def validateI2cControllerTransfer(metadata: dict, result: SystemMessage, isWrite: bool):
    """
    This function validates the metadata for the commands that transfer data using the I2C controller.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        System message to be updated.
    isWrite : bool
        Flag that indicates if the transfer is a write operation. Otherwise, it is a read operation.

    """
    if (metadata["is10BitTargetAddress"] and not check_range(metadata["targetAddress"], int, I2C_MIN_ADDRESS, I2C_MAX_10_BIT_ADDRESS)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong target address value. For 10-bit target address, the valid range is 0x000 - 0x3FF"
    if (not check_type(metadata["registerAddress"], list)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for register address value"
    if metadata["is10BitTargetAddress"] and not check_byte_array(metadata["registerAddress"], I2C_10_BIT_REGISTER_ADDRESS_MAX_LENGTH):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = f"ARGUMENT ERROR: wrong register address array. For 10-bit target address, the register address must be a list of bytes (0x00 - 0xFF) with a maximum length of {I2C_10_BIT_REGISTER_ADDRESS_MAX_LENGTH} bytes"
    if not metadata["is10BitTargetAddress"] and not check_byte_array(metadata["registerAddress"], I2C_7_BIT_REGISTER_ADDRESS_MAX_LENGTH):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = f"ARGUMENT ERROR: wrong register address array. For 7-bit target address, the register address must be a list of bytes (0x00 - 0xFF) with a maximum length of {I2C_7_BIT_REGISTER_ADDRESS_MAX_LENGTH} bytes"
    if isWrite:
        if not check_type(metadata["data"], list):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = "ARGUMENT ERROR: wrong type for data array"
        if not check_byte_array(metadata["data"], MAX_I2C_TRANSFER_LENGTH):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = f"ARGUMENT ERROR: wrong data array. The data must be a list of bytes (0x00 - 0xFF) with a maximum length of {MAX_I2C_TRANSFER_LENGTH} bytes"
    else:
        if (not check_range(metadata["dataLength"], int, 0, MAX_I2C_TRANSFER_LENGTH)):
            result.opcode = RequestValidatorOpcode.FAIL
            result.message = f"ARGUMENT ERROR: wrong data length value. The valid range is 0 - {MAX_I2C_TRANSFER_LENGTH}" 

# endregion

#===============================================================================
# region Validators
#===============================================================================

def i2cControllerInitValidator(metadata: dict):
    """
    This function validates the metadata for the I2C CONTROLLER INIT command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C CONTROLLER INIT request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["busId"], I2cBus)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for I2C Bus value"

    validateI2cControllerConfiguration(metadata, result)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i2cControllerInitSerializer(metadata["id"], metadata["busId"], metadata["frequency_Hz"], metadata["pullUpValue"])

    return request, response, result

def i2cControllerSetParametersValidator(metadata: dict):
    """
    This function validates the metadata for the I2C SET PARAMETERS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C SET PARAMETERS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["busId"], I2cBus)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for I2C Bus value"
    
    validateI2cControllerConfiguration(metadata, result)
    
    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i2cControllerSetParametersSerializer(metadata["id"], metadata["busId"], metadata["frequency_Hz"], metadata["pullUpValue"])

    return request, response, result

def i2cSetPullUpResistorsValidator(metadata: dict):
    """
    This function validates the metadata for the I2C SET PULL UP RESISTORS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C SET PULL UP RESISTORS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["busId"], I2cBus)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for I2C Bus value"
    if (not check_type(metadata["pullUpResistorsValue"], I2cPullUpResistorsValue)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pull up resistors value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i2cSetPullUpResistorsSerializer(metadata["id"], metadata["busId"], metadata["pullUpResistorsValue"])

    return request, response, result

def i2cControllerWriteValidator(metadata: dict):
    """
    This function validates the metadata for the I2C CONTROLLER WRITE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C CONTROLLER WRITE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["busId"], I2cBus)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for I2C Bus value"

    validateI2cControllerTransfer(metadata, result, isWrite=True)
    
    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i2cControllerWriteSerializer(metadata["id"], metadata["busId"], metadata["targetAddress"],
                                                         metadata["registerAddress"], metadata["data"], metadata["isNonStop"], metadata["is10BitTargetAddress"])

    return request, response, result

def i2cControllerReadValidator(metadata: dict):
    """
    This function validates the metadata for the I2C CONTROLLER READ command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C CONTROLLER READ request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["busId"], I2cBus)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for I2C Bus value"

    validateI2cControllerTransfer(metadata, result, isWrite=False)
    
    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i2cControllerReadSerializer(metadata["id"], metadata["busId"], metadata["targetAddress"],
                                                        metadata["dataLength"], metadata["registerAddress"], metadata["is10BitTargetAddress"])

    return request, response, result

def i2cControllerScanBusValidator(metadata: dict):
    """
    This function validates the metadata for the I2C CONTROLLER SCAN BUS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "I2C CONTROLLER SCAN BUS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["busId"], I2cBus)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for I2C Bus value"
    
    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = i2cControllerScanBusSerializer(metadata["id"], metadata["busId"], metadata["include10BitAddresses"])

    return request, response, result

# endregion