from .serializers import *
from ..helpers.validator import check_type, check_valid_id
from ...utils.system_message import SystemMessage, SystemModules, RequestValidatorOpcode

#===============================================================================
# region Validators
#===============================================================================

def gpioConfigurePinValidator(metadata: dict):
    """
    This function validates the metadata for the GPIO CONFIGURE PIN command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO CONFIGURE PIN request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["pinNumber"], GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pin number value"
    if (not check_type(metadata["functionality"], GpioFunctionality)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for functionality value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = gpioConfigurePinSerializer(metadata["id"], metadata["pinNumber"], metadata["functionality"])

    return request, response, result

def gpioDigitalWriteValidator(metadata: dict):
    """
    This function validates the metadata for the GPIO DIGITAL WRITE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO DIGITAL WRITE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["pinNumber"], GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pin number value"
    if (not check_type(metadata["logicLevel"], GpioLogicLevel)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for logic level value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = gpioDigitalWriteSerializer(metadata["id"], metadata["pinNumber"], metadata["logicLevel"])

    return request, response, result

def gpioDigitalReadValidator (metadata: dict):
    """
    This function validates the metadata for the GPIO DIGITAL READ command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO DIGITAL READ request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["pinNumber"], GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pin number value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = gpioDigitalReadSerializer(metadata["id"], metadata["pinNumber"])

    return request, response, result

def gpioSetInterruptValidator (metadata: dict):
    """
    This function validates the metadata for the GPIO SET INTERRUPT command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO SET INTERRUPT request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["pinNumber"], GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pin number value"
    if (not check_type(metadata["trigger"], GpioTriggerType)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for the trigger value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = gpioSetInterruptSerializer(metadata["id"], metadata["pinNumber"],metadata["trigger"])

    return request, response, result

def gpioDisableInterruptValidator (metadata: dict):
    """
    This function validates the metadata for the GPIO DISABLE INTERRUPT command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result =  SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GPIO DISABLE INTERRUPT request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["pinNumber"], GpioPinNumber)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for pin number value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = gpioDisableInterruptSerializer(metadata["id"], metadata["pinNumber"])

    return request, response, result

# endregion