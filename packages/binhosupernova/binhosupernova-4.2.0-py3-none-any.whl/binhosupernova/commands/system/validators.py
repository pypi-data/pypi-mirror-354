from .serializers import *
from ..helpers.validator import check_type, check_valid_id, check_range
from ...utils.system_message import SystemMessage, SystemModules, RequestValidatorOpcode

#===============================================================================
# region Validators
#===============================================================================

def resetDeviceValidator(metadata: dict):
    """
    This function validates the metadata for the RESET DEVICE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "RESET DEVICE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = resetDeviceSerializer(metadata["id"])

    return request, response, result

def enterBootModeValidator(metadata: dict):
    """
    This function validates the metadata for the ENTER BOOT MODE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "ENTER BOOT MODE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = enterBootModeSerializer(metadata["id"])

    return request, response, result

def enterIspModeValidator(metadata: dict):
    """
    This function validates the metadata for the ENTER ISP MODE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "ENTER ISP MODE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = enterIspModeSerializer(metadata["id"])

    return request, response, result

def getUsbStringValidator(metadata: dict):
    """
    This function validates the metadata for the GET USB STRING command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GET USB STRING request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["subcommand"], GetUsbStringSubCommand)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for subcommand value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = getUsbStringSerializer(metadata["id"], metadata["subcommand"])

    return request, response, result

def setI3cVoltageValidator(metadata: dict):
    """
    This function validates the metadata for the SET I3C VOLTAGE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SET I3C VOLTAGE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (metadata["voltage_mV"]!=POWER_OFF_VOLTAGE) and (not check_range(metadata["voltage_mV"], int, MIN_I3C_VOLTAGE_VALUE, MAX_I3C_VOLTAGE_VALUE)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: voltage value out of range"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = setI3cVoltageSerializer(metadata["id"], metadata["voltage_mV"])

    return request, response, result

def setI2cSpiUartGpioVoltValidator(metadata: dict):
    """
    This function validates the metadata for the SET I2C SPI UART GPIO VOLTAGE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SET I2C SPI UART GPIO VOLTAGE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (metadata["voltage_mV"]!=POWER_OFF_VOLTAGE) and (not check_range(metadata["voltage_mV"], int, MIN_I2C_SPI_UART_GPIO_VOLTAGE_VALUE, MAX_I2C_SPI_UART_GPIO_VOLTAGE_VALUE)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: voltage value out of range"
    if (not check_type(metadata["save"],bool)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for save value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = setI2cSpiUartGpioVoltageSerializer(metadata["id"], metadata["voltage_mV"],  metadata["save"])

    return request, response, result

def useExternalI3cVoltageValidator(metadata: dict):
    """
    This function validates the metadata for the USE EXT SRC I3C VOLTAGE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "USE EXT SRC I3C VOLTAGE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = useExternalI3cVoltageSerializer(metadata["id"])

    return request, response, result

def useExternalI2cSpiUartGpioVoltageValidator(metadata: dict):
    """
    This function validates the metadata for the USE EXT SRC I2C-SPI-UART-GPIO VOLTAGE command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "USE EXT SRC I2C-SPI-UART-GPIO VOLTAGE request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["save"],bool)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for save value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = useExternalI2cSpiUartGpioVoltageSerializer(metadata["id"], metadata["save"])

    return request, response, result

def getAnalogMeasurementsValidator(metadata: dict):
    """
    This function validates the metadata for the GET ANALOG MEASUREMENTS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GET ANALOG MEASUREMENTS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = getAnalogMeasurementsSerializer(metadata["id"])

    return request, response, result

def getI3cConnectorsStatusValidator(metadata: dict):
    """
    This function validates the metadata for the GET I3C CONNECTORS STATUS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GET I3C CONNECTORS STATUS request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = getI3cConnectorsStatusSerializer(metadata["id"])

    return request, response, result

def getDeviceInfoValidator(metadata: dict):
    """
    This function validates the metadata for the GET DEVICE INFO command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "GET DEVICE INFO request success")
    request = None
    response = None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = getDeviceInfoSerializer(metadata["id"])

    return request, response, result

# endregion
