from .definitions import *

def gpioConfigurePinSerializer(id: c_uint16, pinNumber: GpioPinNumber, functionality: GpioFunctionality) -> tuple[bytes, GpioConfigurePinResponse_t]:
    """
    This function creates the associated command for configuring a GPIO pin and sends it to the target device.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    pinNumber : GpioPinNumber
        The GPIO pin number to be configured. Must be one of the options provided by the GpioPinNumber enum.
    functionality : GpioFunctionality
        The desired functionality of the GPIO pin, chosen from the options available in the GpioFunctionality enum.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GpioConfigurePinRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = GpioCommandCodes.GPIO_CONFIGURE_PIN.value
    command.fields.parameters.pinNumber = pinNumber.value
    command.fields.parameters.functionality = functionality.value

    return command.toBytes(), GpioConfigurePinResponse_t()

def gpioDigitalWriteSerializer(id: c_uint16, pinNumber: GpioPinNumber, logicLevel: GpioLogicLevel) -> tuple[bytes, GpioDigitalWriteResponse_t]:
    """
    This function creates the associated command for setting the digital logic level of a GPIO pin and sends it to the target device.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    pinNumber : GpioPinNumber
        The GPIO pin number where the digital logic level will be set. Must be one of the options provided by the GpioPinNumber enum.
    logicLevel : GpioLogicLevel
        The desired logic level (HIGH or LOW) to be set on the specified GPIO pin. Selected from the options available in the GpioLogicLevel enum.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GpioDigitalWriteRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = GpioCommandCodes.GPIO_DIGITAL_WRITE.value
    command.fields.parameters.pinNumber = pinNumber.value
    command.fields.parameters.logicLevel = logicLevel.value

    return command.toBytes(), GpioDigitalWriteResponse_t()

def gpioDigitalReadSerializer(id: c_uint16, pinNumber: GpioPinNumber) -> tuple[bytes, GpioDigitalReadResponse_t]:
    """
    This function creates the associated command for reading the digital logic level of a GPIO pin and sends it to the target device.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    pinNumber : GpioPinNumber
        The GPIO pin number where the digital logic level will be set. Must be one of the options provided by the GpioPinNumber enum.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GpioDigitalReadRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = GpioCommandCodes.GPIO_DIGITAL_READ.value
    command.fields.parameters.pinNumber = pinNumber.value

    return command.toBytes(), GpioDigitalReadResponse_t()

def gpioSetInterruptSerializer(id: c_uint16, pinNumber: GpioPinNumber, trigger: GpioTriggerType) -> tuple[bytes, GpioSetInterruptResponse_t]:
    """
    This function creates the associated command for setting an interruption of a GPIO pin and sends it to the target device.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    pinNumber : GpioPinNumber
        The GPIO pin number where the digital logic level will be set. Must be one of the options provided by the GpioPinNumber enum.
    trigger : GpioTriggerType
        The trigger type used for the interruption. Must be one of the options provided by the GpioTriggerType enum.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GpioSetInterruptRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = GpioCommandCodes.GPIO_SET_INTERRUPT.value
    command.fields.parameters.pinNumber = pinNumber.value
    command.fields.parameters.trigger = trigger.value

    return command.toBytes(), GpioSetInterruptResponse_t()

def gpioDisableInterruptSerializer(id: c_uint16, pinNumber: GpioPinNumber) -> tuple[bytes, GpioDisableInterruptResponse_t]:
    """
    This function creates the associated command for disabling an interruption of a GPIO pin and sends it to the target device.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    pinNumber : GpioPinNumber
        The GPIO pin number where the digital logic level will be set. Must be one of the options provided by the GpioPinNumber enum.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GpioDisableInterruptRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = GpioCommandCodes.GPIO_DISABLE_INTERRUPT.value
    command.fields.parameters.pinNumber = pinNumber.value

    return command.toBytes(), GpioDisableInterruptResponse_t()