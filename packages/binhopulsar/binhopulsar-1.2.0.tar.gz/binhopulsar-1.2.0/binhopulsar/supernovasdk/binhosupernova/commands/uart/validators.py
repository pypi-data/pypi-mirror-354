from .serializers import *
from ..helpers.validator import check_type, check_valid_id, check_byte_array
from ...utils.system_message import SystemMessage, SystemModules, RequestValidatorOpcode

#===============================================================================
# region Helper functions
#===============================================================================

def validateUartConfiguration(metadata: dict, result: SystemMessage):
    """
    This function validates the metadata for the commands that configure the UART.
    
    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        SystemMessage to be updated.
    
    """
    if (not check_type(metadata["baudRate"], UartBaudRate)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for baudrate value"
    if (not check_type(metadata["hardwareHandshake"], bool)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for hardware handshake value"
    if (not check_type(metadata["parityMode"], UartParity)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for parity mode value"
    if (not check_type(metadata["dataSize"], UartDataSize)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for data size value"
    if (not check_type(metadata["stopBitType"], UartStopBit)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for stop byte configuration value"

# endregion

#===============================================================================
# region Validators
#===============================================================================

def uartInitValidator(metadata: dict):
    """
    This function validates the metadata for the UART INIT command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "UART INIT request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    
    validateUartConfiguration(metadata, result)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = uartInitSerializer(metadata["id"], metadata["baudRate"], metadata["hardwareHandshake"], metadata["parityMode"], metadata["dataSize"], metadata["stopBitType"])

    return request, response, result

def uartSetParametersValidator(metadata: dict):
    """
    This function validates the metadata for the UART SET PARAMETERS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "UART SET PARAMETERS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    validateUartConfiguration(metadata, result) 

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = uartSetParametersSerializer(metadata["id"], metadata["baudRate"], metadata["hardwareHandshake"], metadata["parityMode"], metadata["dataSize"], metadata["stopBitType"])

    return request, response, result

def uartSendValidator(metadata: dict):
    """
    This function validates the metadata for the UART SEND MESSAGE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "UART SEND MESSAGE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["data"], list)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for data array"
    if (not check_byte_array(metadata["data"], MAX_UART_TRANSFER_LENGTH)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: data length or data type error"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = uartSendSerializer(metadata["id"], metadata["data"])

    return request, response, result

# endregion