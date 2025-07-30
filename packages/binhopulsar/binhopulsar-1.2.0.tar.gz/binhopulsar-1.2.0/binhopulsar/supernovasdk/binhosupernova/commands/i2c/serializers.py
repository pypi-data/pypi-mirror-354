from .definitions import *

def i2cControllerInitSerializer(id: c_uint16, busId: I2cBus, frequency_Hz: int, pullUpValue: I2cPullUpResistorsValue) -> tuple[bytes, I2cControllerInitResponse_t]:
    """
    This function performs an I2C_CONTROLLER_INIT command, sending the selected I2C bus
    to initialize and values to set frequency (I2C SCL frequency) and pull up resistors.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    busId : I2cBus
        Selected I2C Bus to initialize.
    frequency_Hz : int
        Numerical value that represents the desired I2C SCL frequency in Hz. Currently, the minimum allowed value
        is 100000 Hz and the maximum allowed value is 1000000 Hz.
    pullUpValue : I2cPullUpResistorsValue
        Value of the pull up enum that represents the desired Pull Up resistors value

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = I2cControllerInitRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = I2cCommandCodes.I2C_CONTROLLER_INIT.value
    command.fields.parameters.busId = busId.value
    command.fields.parameters.frequency_Hz = frequency_Hz
    command.fields.parameters.pullUpValue = pullUpValue.value

    # Return command
    return command.toBytes(), I2cControllerInitResponse_t()

def i2cControllerSetParametersSerializer(id: c_uint16, busId: I2cBus, frequency_Hz: int, pullUpValue: I2cPullUpResistorsValue) -> tuple[bytes, I2cControllerSetParametersResponse_t]:
    """
    This function performs an I2C_SET_PARAMETERS command, sending the selected I2C bus
    to configure and values to set frequency (I2C SCL frequency) and pull up resistors.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    busId : I2cBus
        Selected I2C Bus to set parameters.
    frequency_Hz : int
        Numerical value that represents the desired I2C SCL frequency in Hz. Currently, the minimum allowed value
            is 100000 Hz and the maximum allowed value is 1000000 Hz.
    pullUpValue : I2cPullUpResistorsValue
        Value of the pull up enum that represents the desired Pull Up resistors value.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = I2cControllerSetParametersRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = I2cCommandCodes.I2C_CONTROLLER_SET_PARAMETERS.value
    command.fields.parameters.busId = busId.value
    command.fields.parameters.frequency_Hz = frequency_Hz
    command.fields.parameters.pullUpValue = pullUpValue.value

    # Return command
    return command.toBytes(), I2cControllerSetParametersResponse_t()

def i2cSetPullUpResistorsSerializer(id: c_uint16, busId: I2cBus, pullUpValue: I2cPullUpResistorsValue) -> tuple[bytes, I2cSetPullUpResistorsResponse_t]:
    """
    This function performs an I2C_SET_PULL_UP_RESISTORS command, sending the selected pull up
    resistor value for the I2C lines.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    busId : I2cBus
        Selected I2C Bus to set pull up resistors.
    pullUpValue : I2cPullUpResistorsValue
        This parameter represents the different values for the pull up resistors.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = I2cSetPullUpResistorsRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = I2cCommandCodes.I2C_SET_PULLUP_RESISTORS.value
    command.fields.parameters.busId = busId.value
    command.fields.parameters.pullUpValue = pullUpValue.value

    # Return command
    return command.toBytes(), I2cSetPullUpResistorsResponse_t()

def i2cControllerWriteSerializer(id: c_uint16, busId: I2cBus, targetAddress: int, registerAddress: list, payload: list, isNonStop: bool, is10BitTargetAddress: bool) -> tuple[bytes, I2cControllerTransferResponse_t]:
    """
    This function is used to generate the I2C_CONTROLLER_WRITE command.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    busId : int
        Selected I2C Bus to write data.
    targetAddress : int
        7-bit slave address
    registerAddress : list
        List that represents the subaddress/register address. It can contains
        up to 4 bytes.
    payload : list
        List containing bytes to transfer.
    isNonStop : bool
        This parameter is used to indicate if the transaction is non-stop.
    is10BitTargetAddress : bool
        This parameter is used to indicate if the target address is 10-bit.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = I2cControllerTransferRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = I2cCommandCodes.I2C_CONTROLLER_WRITE.value

    # I2C Bus
    command.fields.parameters.busId = busId.value

    # Transfer Length
    command.fields.parameters.transfLength = len(payload)

    # 10-bit address
    if is10BitTargetAddress:
        # Two MSB of the target address
        command.fields.parameters.targetAddress = I2C_10_BIT_ADDRESS_FIRST_BYTE_MASK | (targetAddress >> I2C_10_BIT_ADDRESS_FIRST_BYTE_SHIFT)

        # 8 LSB of the target address
        command.fields.parameters.registerAddress = c_uint32(targetAddress & I2C_10_BIT_ADDRESS_SECOND_BYTE_MASK)
        command.fields.parameters.registerAddressLength = 1

    else:
        # 7-bit address
        command.fields.parameters.targetAddress = targetAddress

    # Register address length
    registerAddressLength = len(registerAddress)
    command.fields.parameters.registerAddressLength += registerAddressLength

    # Register address
    for i in range(registerAddressLength):
        command.fields.parameters.registerAddress = c_uint32(command.fields.parameters.registerAddress << 8 | registerAddress[i])

    # Payload
    for i in range(len(payload)):
        command.fields.payload[i] = payload[i]
    
    # Non-stop
    command.fields.parameters.isNonStop = isNonStop

    # Return command structure.
    return command.toBytes(), I2cControllerTransferResponse_t()

def i2cControllerReadSerializer(id: c_uint16, busId: I2cBus, targetAddress: int, length: int, registerAddress: list, is10BitTargetAddress: bool) -> tuple[bytes, I2cControllerTransferResponse_t]:
    """
    This function is used to generate the I2C_CONTROLLER_READ command.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    busId : I2cBus
        Selected I2C Bus to read data.
    targetAddress : int
        7-bit slave address
    length : int
        Length of data to be read from the USB device.
    registerAddress : list
        List that represents the subaddress/register address. It can contains
        up to 4 bytes.
    is10BitTargetAddress : bool
        This parameter is used to indicate if the target address is 10-bit.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = I2cControllerTransferRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = I2cCommandCodes.I2C_CONTROLLER_READ.value

    # I2C Bus
    command.fields.parameters.busId = busId.value

    # Transfer Length
    command.fields.parameters.transfLength = length

    # 10-bit address
    if is10BitTargetAddress:
        # Two MSB bits of the target address
        command.fields.parameters.targetAddress = I2C_10_BIT_ADDRESS_FIRST_BYTE_MASK | (targetAddress >> I2C_10_BIT_ADDRESS_FIRST_BYTE_SHIFT)

        # 8-bit LSB of the target address
        command.fields.parameters.registerAddress = c_uint32(targetAddress & I2C_10_BIT_ADDRESS_SECOND_BYTE_MASK)
        command.fields.parameters.registerAddressLength = 1

    else:
        # 7-bit address
        command.fields.parameters.targetAddress = targetAddress

    # Register address length
    registerAddressLength = len(registerAddress)
    command.fields.parameters.registerAddressLength += registerAddressLength

    # Register address
    for i in range(registerAddressLength):
        command.fields.parameters.registerAddress = c_uint32(command.fields.parameters.registerAddress << 8 | registerAddress[i])

    # Return command structure.
    return command.toBytes(), I2cControllerTransferResponse_t()

def i2cControllerScanBusSerializer(id: c_uint16, busId: I2cBus, include10BitAddresses: bool) -> tuple[bytes, I2cControllerScanBusResponse_t]:
    """
    This function is used to generate the I2C_CONTROLLER_SCAN_BUS command.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    busId : I2cBus
        Selected I2C Bus to scan.
    include10BitAddresses : bool
        This parameter is used to indicate if the scan should include 10-bit addresses.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = I2cControllerScanBusRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = I2cCommandCodes.I2C_CONTROLLER_SCAN_BUS.value
    command.fields.parameters.busId = busId.value
    command.fields.parameters.include10BitAddresses = include10BitAddresses

    # Return command structure.
    return command.toBytes(), I2cControllerScanBusResponse_t()
