from .serializers import *
from ..helpers.validator import check_type, check_valid_id, check_byte_array, check_range
from ...utils.system_message import SystemMessage, SystemModules, RequestValidatorOpcode

#===============================================================================
# region Helper functions
#===============================================================================

def validateSpiControllerConfiguration(metadata: dict, result: SystemMessage):
    """
    This function validates the metadata for the commands that configure the SPI controller.
    
    Arguments
    ---------
    metadata : dict
        Metadata to be validated.
    result : SystemMessage
        SystemMessage to be updated.
    
    """
    if (not check_range(metadata["frequency"], int, SPI_CONTROLLER_MIN_FREQUENCY, SPI_CONTROLLER_MAX_FREQUENCY)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: frequency value out of range"
    if (not check_type(metadata["bitOrder"], SpiControllerBitOrder)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for bitOrder value"
    if (not check_type(metadata["mode"], SpiControllerMode)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for mode value"
    if (not check_type(metadata["dataWidth"], SpiControllerDataWidth)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for dataWidth value"
    if (not check_type(metadata["chipSelect"], SpiControllerChipSelect)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for chipSelect value"
    if (not check_type(metadata["chipSelectPol"], SpiControllerChipSelectPolarity)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for chipSelectPol value"

# endregion

#===============================================================================
# region Validators
#===============================================================================

def spiControllerInitValidator(metadata: dict):
    """
    This function validates the metadata for the SPI CONTROLLER INIT command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SPI CONTROLLER INIT request success")
    request, response = None, None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    
    validateSpiControllerConfiguration(metadata, result)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = spiControllerInitSerializer(metadata["id"], metadata["bitOrder"], metadata["mode"], metadata["dataWidth"], metadata["chipSelect"], metadata["chipSelectPol"], metadata["frequency"])

    return request, response, result

def spiControllerSetParametersValidator(metadata: dict):
    """
    This function validates the metadata for the SPI CONTROLLER SET PARAMETERS command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SPI CONTROLLER SET PARAMETERS request success")
    request, response = None, None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    
    validateSpiControllerConfiguration(metadata, result)

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = spiControllerSetParametersSerializer(metadata["id"], metadata["bitOrder"], metadata["mode"], metadata["dataWidth"], metadata["chipSelect"], metadata["chipSelectPol"], metadata["frequency"])

    return request, response, result

def spiControllerTransferValidator(metadata: dict):
    """
    This function validates the metadata for the SPI CONTROLLER TRANSFER command.

    Arguments
    ---------
    metadata : dict
        Metadata to be validated.

    Returns
    -------
    tuple
        A tuple containing the request, response and result of the validation.

    """
    result = SystemMessage(SystemModules.VALIDATION, RequestValidatorOpcode.SUCCESS, "SPI CONTROLLER TRANSFER request success")
    request, response = None, None

    if (not check_valid_id(metadata["id"])):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong id value"
    if (not check_type(metadata["payload"], list)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: wrong type for payload value"
    if (not check_byte_array(metadata["payload"], MAX_SPI_TRANSFER_LENGTH)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: payload length or data type error"
    if (not check_range(metadata["transferLength"], int, 1, MAX_SPI_TRANSFER_LENGTH)):
        result.opcode = RequestValidatorOpcode.FAIL
        result.message = "ARGUMENT ERROR: transferLength value out of range"

    if (result.opcode == RequestValidatorOpcode.SUCCESS):
        request, response = spiControllerTransferSerializer(metadata["id"], metadata["transferLength"], metadata["payload"])

    return request, response, result

# endregion