from ..common_definitions import *

#================================================================================#
# region SPI COMMAND DEFINITIONS
#================================================================================#

class SpiCommandCodes(Enum):
    """
    Enumeration of the SPI command codes.
    """
    SPI_DEINIT                      = makeCommandCode(Group.SPI.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 1)
    SPI_CONTROLLER_INIT             = makeCommandCode(Group.SPI.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 1)
    SPI_CONTROLLER_SET_PARAMETERS   = makeCommandCode(Group.SPI.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 2)
    SPI_CONTROLLER_GET_PARAMETERS   = makeCommandCode(Group.SPI.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 3)
    SPI_CONTROLLER_TRANSFER         = makeCommandCode(Group.SPI.value, CommandRole.CONTROLLER.value, CommandType.REQUEST_RESPONSE.value, 4)

SPI_COMMAND_NAMES = {
    result.value: result.name.replace("_", " ") for result in SpiCommandCodes
}

# endregion

#================================================================================#
# region SPI COMMON DEFINITIONS
#================================================================================#

# SPI Bus Configuration
SPI_CONTROLLER_MIN_FREQUENCY = 10000       # In Hz -> 10 kHz
SPI_CONTROLLER_MAX_FREQUENCY = 50000000    # In Hz -> 50 MHz

class SpiControllerBitOrder(Enum):
    MSB    = 0x00
    LSB    = 0x01

class SpiControllerMode(Enum):
    MODE_0    = 0x00
    MODE_1    = 0x01
    MODE_2    = 0x02
    MODE_3    = 0x03

class SpiControllerDataWidth(Enum):
    _8_BITS_DATA    = 0x00
    _16_BITS_DATA   = 0x01

class SpiControllerChipSelect(Enum):
    CHIP_SELECT_0   = 0x00
    CHIP_SELECT_1   = 0x01
    CHIP_SELECT_2   = 0x02
    CHIP_SELECT_3   = 0x03

class SpiControllerChipSelectPolarity(Enum):
    ACTIVE_LOW  = 0x00
    ACTIVE_HIGH = 0x01

class SpiControllerConfigurationParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("bitOrder", c_uint8),
                ("mode", c_uint8),
                ("dataWidth", c_uint8),
                ("chipSelect", c_uint8),
                ("chipSelectPol", c_uint8),
                ("frequency", c_uint32)]

# endregion

#================================================================================#
# region SPI CONTROLLER INIT
#================================================================================#

# Request ---------------------------------------------------------------------- #

class SpiControllerInitRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", SpiControllerConfigurationParameters_t)]

SpiControllerInitRequestArray_t = c_uint8 * sizeof(SpiControllerInitRequestFields_t)

class SpiControllerInitRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", SpiControllerInitRequestArray_t ),
                ("fields", SpiControllerInitRequestFields_t )]

# Response --------------------------------------------------------------------- #

class SpiControllerInitResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

SpiControllerInitResponseArray_t = c_uint8 * sizeof(SpiControllerInitResponseFields_t)

class SpiControllerInitResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", SpiControllerInitResponseArray_t ),
                ("fields", SpiControllerInitResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = SpiControllerInitResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        """
        This function returns a dictionary with the response fields.
        """
        return {
            "id": self.fields.header.id,
            "command": SPI_COMMAND_NAMES[self.fields.header.code],
            "result": COMMON_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region SPI CONTROLLER SET PARAMETERS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class SpiControllerSetParameterRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", SpiControllerConfigurationParameters_t)]

SpiControllerSetParameterRequestArray_t = c_uint8 * sizeof(SpiControllerSetParameterRequestFields_t)

class SpiControllerSetParameterRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", SpiControllerSetParameterRequestArray_t ),
                ("fields", SpiControllerSetParameterRequestFields_t )]

# Response --------------------------------------------------------------------- #

class SpiControllerSetParameterResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

# Union array
SpiControllerSetParameterResponseArray_t = c_uint8 * sizeof(SpiControllerSetParameterResponseFields_t)

class SpiControllerSetParameterResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", SpiControllerSetParameterResponseArray_t ),
                ("fields", SpiControllerSetParameterResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        self.data = SpiControllerSetParameterResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        """
        This function returns a dictionary with the response fields.
        """
        return {
            "id": self.fields.header.id,
            "command": SPI_COMMAND_NAMES[self.fields.header.code],
            "result": COMMON_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region SPI CONTROLLER TRANSFER
#================================================================================#

MAX_SPI_TRANSFER_LENGTH = 1024

# Request ---------------------------------------------------------------------- #

class SpiControllerTransferRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("payloadLength", c_uint16),
                ("transferLength", c_uint16)]

SpiControllerTransferRequestPayload_t = c_uint8 * MAX_SPI_TRANSFER_LENGTH

class SpiControllerTransferRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", SpiControllerTransferRequestParameters_t),
                ("payload", SpiControllerTransferRequestPayload_t)]

SpiControllerTransferRequestArray_t = c_uint8 * sizeof(SpiControllerTransferRequestFields_t)

class SpiControllerTransferRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", SpiControllerTransferRequestArray_t ),
                ("fields", SpiControllerTransferRequestFields_t )]

    def toBytes(self) -> bytes:
        """
        Method to return an bytes object representing the command
        serialization.
        """
        length = sizeof(CommandRequestHeader_t) + sizeof(SpiControllerTransferRequestParameters_t) + self.fields.parameters.payloadLength
        return bytes(self.data[:length])

# Response --------------------------------------------------------------------- #

class SpiControllerTransferResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("payloadLength", c_uint16)]

SpiControllerTransferResponsePayload_t = c_uint8 * MAX_SPI_TRANSFER_LENGTH

class SpiControllerTransferResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", SpiControllerTransferResponseParameters_t),
                ("payload", SpiControllerTransferResponsePayload_t)]

SpiControllerTransferResponseArray_t = c_uint8 * sizeof(SpiControllerTransferResponseFields_t)

class SpiControllerTransferResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", SpiControllerTransferResponseArray_t ),
                ("fields", SpiControllerTransferResponseFields_t )]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a data buffer.
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:
        """
        This function returns a dictionary with the response fields.
        """
        return {
            "id": self.fields.header.id,
            "command": SPI_COMMAND_NAMES[self.fields.header.code],
            "result": COMMON_RESULT_NAMES[self.fields.header.result],
            "payload_length": self.fields.parameters.payloadLength,
            "payload": self.fields.payload[:self.fields.parameters.payloadLength]
        }

# endregion