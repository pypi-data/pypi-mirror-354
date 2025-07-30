from .definitions import *

def spiControllerInitSerializer(id: c_uint16,
                                 bitOrder: SpiControllerBitOrder,
                                 mode: SpiControllerMode,
                                 dataWidth: SpiControllerDataWidth,
                                 chipSelect: SpiControllerChipSelect,
                                 chipSelectPol: SpiControllerChipSelectPolarity,
                                 frequency: c_uint32) -> tuple[bytes, SpiControllerInitResponse_t]:
    """
    This function performs a SPI_CONTROLLER_INIT command, sending configuration data to
    initialize the SPI controller.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    bitOrder: SpiControllerBitOrder
        Sets the bit's order of the transfer. It could be MSB or LSB first.
    mode: SpiControllerMode
        Sets the transfer mode: Mode 0, Mode 1, Mode 2 or Mode 3.
    dataWidth: SpiControllerDataWidth
        Sets the data width of the transfer. It could be 8 or 16 bits.
    chipSelect: SpiControllerChipSelect
        Sets the chip select to be used: Chip Select 0, Chip Select 1, Chip Select 2 or Chip Select 3.
    chipSelectPol : SpiControllerChipSelectPolarity
        Sets the chip select polarity: Active Low or Active High.
    frequency : c_uint32
        Value of frequency to be set in the SPI controller expressed in Hz.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = SpiControllerInitRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SpiCommandCodes.SPI_CONTROLLER_INIT.value
    command.fields.parameters.bitOrder = bitOrder.value
    command.fields.parameters.mode = mode.value
    command.fields.parameters.dataWidth = dataWidth.value
    command.fields.parameters.chipSelect = chipSelect.value
    command.fields.parameters.chipSelectPol = chipSelectPol.value
    command.fields.parameters.frequency = frequency

    return command.toBytes(), SpiControllerInitResponse_t()

def spiControllerSetParametersSerializer(id: c_uint16,
                                         bitOrder: SpiControllerBitOrder,
                                         mode: SpiControllerMode,
                                         dataWidth: SpiControllerDataWidth,
                                         chipSelect: SpiControllerChipSelect,
                                         chipSelectPol: SpiControllerChipSelectPolarity,
                                         frequency: c_uint32) -> tuple[bytes, SpiControllerSetParameterResponse_t]:
    """
    This function performs a SPI_CONTROLLER_SET_PARAMETERS command, sending optional data to
    set bit order, mode, data width, chip select, chip select polarity and clock frequency.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    bitOrder: SpiControllerBitOrder
        Sets the bit's order of the transfer. It could be MSB or LSB first.
    mode: SpiControllerMode
        Sets the transfer mode: Mode 0, Mode 1, Mode 2 or Mode 3.
    dataWidth: SpiControllerDataWidth
        Sets the data width of the transfer. It could be 8 or 16 bits.
    chipSelect: SpiControllerChipSelect
        Sets the chip select to be used: Chip Select 0, Chip Select 1, Chip Select 2 or Chip Select 3.
    chipSelectPol : SpiControllerChipSelectPolarity
        Sets the chip select polarity: Active Low or Active High.
    frequency : c_uint32
        Value of frequency to be set in the SPI controller expressed in Hz.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command instance
    command = SpiControllerSetParameterRequest_t()

    # Fill command fields.
    command.fields.header.id = id
    command.fields.header.code = SpiCommandCodes.SPI_CONTROLLER_SET_PARAMETERS.value
    command.fields.parameters.bitOrder = bitOrder.value
    command.fields.parameters.mode = mode.value
    command.fields.parameters.dataWidth = dataWidth.value
    command.fields.parameters.chipSelect = chipSelect.value
    command.fields.parameters.chipSelectPol = chipSelectPol.value
    command.fields.parameters.frequency = frequency

    return command.toBytes(), SpiControllerSetParameterResponse_t()

def spiControllerTransferSerializer(id: c_uint16,
                                    transferLength: c_uint16,
                                    payload: list) -> tuple[bytes, SpiControllerTransferResponse_t]:
    """
    This function performs a SPI_CONTROLLER_TRANSFER command, sending data to
    the SPI controller.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    transferLength : c_uint16
        Length of the transfer.
    payload : list
        List that contains the data to be sent.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = SpiControllerTransferRequest_t()

    # Set endpoint ID and command opcode.
    command.fields.header.id = id
    command.fields.header.code = SpiCommandCodes.SPI_CONTROLLER_TRANSFER.value
    command.fields.parameters.payloadLength = len(payload)
    command.fields.parameters.transferLength = transferLength

    # Load Payload
    for i in range(command.fields.parameters.payloadLength):
        command.fields.payload[i] = payload[i]

    # Return command
    return command.toBytes(), SpiControllerTransferResponse_t()