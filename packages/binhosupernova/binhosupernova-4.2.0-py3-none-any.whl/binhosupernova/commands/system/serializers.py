from .definitions import *

def resetDeviceSerializer(id: c_uint16) -> tuple[bytes, None]:
    """
    This function generates and returns a RESET DEVICE command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.
        In this case, the response instance is None.

    """
    # Create command instance
    command = ResetDeviceRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_RESET_DEVICE.value

    return command.toBytes(), None

def enterBootModeSerializer(id: c_uint16) -> tuple[bytes, None]:
    """
    This function generates and returns a ENTER BOOT MODE command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.
        In this case, the response instance is None.

    """
    # Create command instance
    command = EnterBootModeRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_ENTER_BOOT_MODE.value

    return command.toBytes(), None

def enterIspModeSerializer(id: c_uint16) -> tuple[bytes, None]:
    """
    This function generates and returns a ENTER ISP MODE command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.
        In this case, the response instance is None.

    """
    # Create command instance
    command = EnterIspModeRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_ENTER_ISP_MODE.value

    return command.toBytes(), None

def getUsbStringSerializer(id: c_uint16, subCommand: GetUsbStringSubCommand) -> tuple[bytes, GetUsbStringResponse_t]:
    """
    This function generates and returns a Get USB String command taking the subcommand
    passed as parameter. Just the subcommands bellow are supported:
    1 - Read Manufacturer Descriptor String
    2 - Read Product Descriptor String
    3 - Read Serial Number Descriptor String
    4 - Read Firmware Version Descriptor String
    5 - Read Hardware Version Descriptor String

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.
    subCommand : int
        Sub-command value.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GetUsbStringRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_GET_USB_STRING.value
    command.fields.parameters.subCommand = subCommand.value

    return command.toBytes(), GetUsbStringResponse_t()

def setI3cVoltageSerializer(id: c_uint16, voltage_mV: c_uint16) -> tuple[bytes, SetI3cVoltageResponse_t]:
    """
    This function generates and returns a Set I3C Voltage command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.
    voltage_mV : c_uint16
        Voltage that wants to be set for the I3C bus.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = SetI3cVoltageRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_SET_I3C_VOLTAGE.value
    command.fields.parameters.voltage_mV = voltage_mV

    return command.toBytes(), SetI3cVoltageResponse_t()

def setI2cSpiUartGpioVoltageSerializer(id: c_uint16, voltage_mV: c_uint16, save: bool) -> tuple[bytes, SetI2cSpiUartGpioVoltageResponse_t]:
    """
    This function generates and returns a Set I2C-SPI-UART-GPIO Voltage command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.
    voltage_mV : c_uint16
        Voltage that wants to be set for the I2C-SPI-UART-GPIO buses.
    save : bool
            It indicates if the bus voltage configuration must be stored in the device non-volatile memory.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = SetI2cSpiUartGpioVoltageRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_SET_I2C_SPI_UART_GPIO_VOLTAGE.value

    command.fields.parameters.voltage_mV = voltage_mV
    command.fields.parameters.save = save

    return command.toBytes(), SetI2cSpiUartGpioVoltageResponse_t()

def useExternalI3cVoltageSerializer(id: c_uint16) -> tuple[bytes, UseExtI3cVoltageResponse_t]:
    """
    This function generates and returns a USE EXT SRC I3C VOLTAGE command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = UseExtI3cVoltageRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_USE_EXTERNAL_I3C_VOLTAGE.value

    return command.toBytes(), UseExtI3cVoltageResponse_t()

def useExternalI2cSpiUartGpioVoltageSerializer(id: c_uint16, save: bool) -> tuple[bytes, UseExternalI2cSpiUartGpioVoltageResponse_t]:
    """
    This function generates and returns a USE EXT SRC I2C-SPI-UART VOLTAGE command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.
    save : bool
            It indicates if the bus voltage configuration must be stored in the device non-volatile memory.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = UseExternalI2cSpiUartGpioVoltageRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_USE_EXTERNAL_I2C_SPI_UART_GPIO_VOLTAGE.value
    command.fields.parameters.save = save

    return command.toBytes(), UseExternalI2cSpiUartGpioVoltageResponse_t()

def getAnalogMeasurementsSerializer(id: c_uint16) -> tuple[bytes, GetAnalogMeasurementsResponse_t]:
    """
    This function generates and returns a Get Analog Measurements command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GetAnalogMeasurementsRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_GET_ANALOG_MEASUREMENTS.value

    return command.toBytes(), GetAnalogMeasurementsResponse_t()

def getI3cConnectorsStatusSerializer(id: c_uint16) -> tuple[bytes, GetI3cConnectorsStatusResponse_t]:
    """
    This function generates and returns a GET I3C CONNECTORS STATUS command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GetI3cConnectorsStatusRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_GET_I3C_CONNECTOR_STATUS.value

    return command.toBytes(), GetI3cConnectorsStatusResponse_t()

def getDeviceInfoSerializer(id: c_uint16) -> tuple[bytes, GetDeviceInfoResponse_t]:
    """
    This function generates and returns a GET DEVICE INFO command

    Argument
    --------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = GetDeviceInfoRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SysCommandCodes.SYS_GET_DEVICE_INFO.value

    return command.toBytes(), GetDeviceInfoResponse_t()