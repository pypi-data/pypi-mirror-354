from ..common_definitions import *

#================================================================================#
# region SYSTEM COMMAND DEFINITIONS
#================================================================================#

class SysCommandCodes(Enum):
    """
    Enumeration of the SYS command codes.
    """
    SYS_RESET_DEVICE                            = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 1)
    SYS_ENTER_BOOT_MODE                         = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 2)
    SYS_ENTER_ISP_MODE                          = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 3)
    SYS_SET_I3C_VOLTAGE                         = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 4)
    SYS_SET_I2C_SPI_UART_GPIO_VOLTAGE           = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 5)
    SYS_SET_1WIRE_VOLTAGE                       = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 6)
    SYS_GET_USB_STRING                          = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 7)
    SYS_GET_I3C_CONNECTOR_STATUS                = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 8)
    SYS_GET_ANALOG_MEASUREMENTS                 = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 9)
    SYS_USE_EXTERNAL_I3C_VOLTAGE                = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 10)
    SYS_USE_EXTERNAL_I2C_SPI_UART_GPIO_VOLTAGE  = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 11)
    SYS_GET_DEVICE_INFO                         = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.REQUEST_RESPONSE.value, 12)
    SYS_I3C_CONNECTOR_EVENT_NOTIFICATION        = makeCommandCode(Group.SYS.value, CommandRole.GENERIC.value, CommandType.NOTIFICATION.value, 1)

SYS_COMMAND_NAMES = {
    result.value: result.name.replace("_", " ") for result in SysCommandCodes
}

# endregion

#================================================================================#
# region SYSTEM COMMON DEFINITIONS
#================================================================================#

POWER_OFF_VOLTAGE = 0

# endregion

#================================================================================#
# region SYSTEM RESULT DEFINITIONS
#================================================================================#

class SysResultCodes(Enum):
    """
    Enumeration of SYS result codes.
    """
    VOLTAGE_OUT_OF_RANGE                = makeResultCode(Group.SYS.value, 1)
    EXTERNAL_VOLTAGE_DETECTED           = makeResultCode(Group.SYS.value, 2)
    VOLTAGE_ADJUSTMENT_FAILURE          = makeResultCode(Group.SYS.value, 3)
    I3C_PORTS_NOT_POWERED               = makeResultCode(Group.SYS.value, 4)
    BOTH_I3C_PORTS_POWERED              = makeResultCode(Group.SYS.value, 5)
    VOLTAGE_OUT_OF_RANGE_ON_I3C_LV      = makeResultCode(Group.SYS.value, 6)
    VOLTAGE_OUT_OF_RANGE_ON_I3C_HV      = makeResultCode(Group.SYS.value, 7)

SYS_RESULT_NAMES = {
    **COMMON_RESULT_NAMES,
    **{result.value: result.name for result in SysResultCodes}
}

# endregion

#================================================================================#
# region RESET DEVICE
#================================================================================#

# Request ---------------------------------------------------------------------- #

class ResetDeviceRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

ResetDeviceRequestArray_t = c_uint8 * sizeof(ResetDeviceRequestFields_t)

class ResetDeviceRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", ResetDeviceRequestArray_t),
                ("fields", ResetDeviceRequestFields_t)]

# endregion

#================================================================================#
# region ENTER BOOT MODE
#================================================================================#

# Request ---------------------------------------------------------------------- #

class EnterBootModeRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

EnterBootModeRequestArray_t = c_uint8 * sizeof(EnterBootModeRequestFields_t)

class EnterBootModeRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", EnterBootModeRequestArray_t),
                ("fields", EnterBootModeRequestFields_t)]

# endregion

#================================================================================#
# region ENTER ISP MODE
#================================================================================#

# Request ---------------------------------------------------------------------- #

class EnterIspModeRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

EnterIspModeRequestArray_t = c_uint8 * sizeof(EnterIspModeRequestFields_t)

class EnterIspModeRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", EnterIspModeRequestArray_t),
                ("fields", EnterIspModeRequestFields_t)]

# endregion

#================================================================================#
# region GET USB STRING
#================================================================================#

class GetUsbStringSubCommand(Enum):
    """
    Enum that represents the USB Descriptors that can be retrieved by GET USB STRING
    command. The values assigned match the string indexes in the string descriptor.
    """
    MANUFACTURER    = 0x01
    PRODUCT_NAME    = 0X02
    SERIAL_NUMBER   = 0x03
    FW_VERSION      = 0x04
    HW_VERSION      = 0x05
    BL_VERSION      = 0x06

# Request ---------------------------------------------------------------------- #

class GetUsbStringRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("subCommand",c_uint8)]

class GetUsbStringRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", GetUsbStringRequestParameters_t)]

GetUsbStringRequestArray_t = c_uint8 * sizeof(GetUsbStringRequestFields_t)

class GetUsbStringRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GetUsbStringRequestArray_t),
                ("fields", GetUsbStringRequestFields_t)]

# Response --------------------------------------------------------------------- #

MAXIMUM_USB_STRING_LENGTH = 50

class GetUsbStringResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("payloadLength", c_uint8)]

GetUsbStringResponsePayload_t = c_uint8 * MAXIMUM_USB_STRING_LENGTH

class GetUsbStringResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", GetUsbStringResponseParameters_t),
                ("payload", GetUsbStringResponsePayload_t)]

GetUsbStringResponseArray_t = c_uint8 * sizeof(GetUsbStringResponseFields_t)

class GetUsbStringResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", GetUsbStringResponseArray_t),
                ("fields", GetUsbStringResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a buffer object
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:

        payload_length = self.fields.parameters.payloadLength - 1
        data = str(self.fields.payload,encoding='ascii')[:payload_length]

        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result],
            "payload_length": payload_length,
            "payload": data
        }


# endregion

#================================================================================#
# region SET I3C VOLTAGE
#================================================================================#

# Constants
MIN_I3C_VOLTAGE_VALUE = 800
MAX_I3C_VOLTAGE_VALUE = 3300

# Request ---------------------------------------------------------------------- #

class SetI3cVoltageRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("voltage_mV" , c_uint16)]

class SetI3cVoltageRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
		        ("parameters" , SetI3cVoltageRequestParameters_t)]

SetI3cVoltageRequestArray_t = c_uint8 * sizeof(SetI3cVoltageRequestFields_t)

class SetI3cVoltageRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", SetI3cVoltageRequestArray_t),
                ("fields", SetI3cVoltageRequestFields_t)]

# Response --------------------------------------------------------------------- #

class SetI3cVoltageResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

# Union array
SetI3cVoltageResponseArray_t = c_uint8 * sizeof(SetI3cVoltageResponseFields_t)

class SetI3cVoltageResponse_t(BaseCommandResponse_t):

    _fields_ = [("data", SetI3cVoltageResponseArray_t),
                ("fields", SetI3cVoltageResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a buffer object
        """
        self.data = SetI3cVoltageResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region SET I2C/SPI/UART/GPIO VOLTAGE
#================================================================================#

# Constants
MIN_I2C_SPI_UART_GPIO_VOLTAGE_VALUE = 1200
MAX_I2C_SPI_UART_GPIO_VOLTAGE_VALUE = 3300

# Request ---------------------------------------------------------------------- #

class SetI2cSpiUartGpioVoltageRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("voltage_mV", c_uint16),
                ("save", c_uint8)]

class SetI2cSpiUartGpioVoltageRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
		        ("parameters" , SetI2cSpiUartGpioVoltageRequestParameters_t),]

SetI2cSpiUartGpioVoltageRequestArray_t = c_uint8 * sizeof(SetI2cSpiUartGpioVoltageRequestFields_t)

class SetI2cSpiUartGpioVoltageRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", SetI2cSpiUartGpioVoltageRequestArray_t),
                ("fields", SetI2cSpiUartGpioVoltageRequestFields_t)]

# Response --------------------------------------------------------------------- #

class SetI2cSpiUartGpioVoltageResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t)]

SetI2cSpiUartGpioVoltageResponseArray_t = c_uint8 * sizeof(SetI2cSpiUartGpioVoltageResponseFields_t)

# Union command
class SetI2cSpiUartGpioVoltageResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", SetI2cSpiUartGpioVoltageResponseArray_t),
                ("fields", SetI2cSpiUartGpioVoltageResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a buffer object
        """
        self.data = SetI2cSpiUartGpioVoltageResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result]
        }

# endregion

#================================================================================#
# region USE EXTERNAL I3C VOLTAGE
#================================================================================#

# Request ---------------------------------------------------------------------- #

class UseExtI3cVoltageRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

UseExtI3cVoltageRequestArray_t = c_uint8 * sizeof(UseExtI3cVoltageRequestFields_t)

class UseExtI3cVoltageRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", UseExtI3cVoltageRequestArray_t),
                ("fields", UseExtI3cVoltageRequestFields_t)]

# Response --------------------------------------------------------------------- #

class UseExtI3cVoltageResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("externalHighVoltage_mV", c_uint16),
                ("externalLowVoltage_mV", c_uint16)]

class UseExtI3cVoltageResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", UseExtI3cVoltageResponseParameters_t)]

UseExtI3cVoltageResponseArray_t = c_uint8 * sizeof(UseExtI3cVoltageResponseFields_t)

class UseExtI3cVoltageResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", UseExtI3cVoltageResponseArray_t),
                ("fields", UseExtI3cVoltageResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a buffer object
        """
        self.data = UseExtI3cVoltageResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result],
            "i3c_low_voltage_mV": self.fields.parameters.externalLowVoltage_mV,
            "i3c_high_voltage_mV": self.fields.parameters.externalHighVoltage_mV
        }

# endregion

#================================================================================#
# region USE EXTERNAL I2C/SPI/UART/GPIO VOLTAGE
#================================================================================#

# Request ---------------------------------------------------------------------- #

class UseExternalI2cSpiUartGpioVoltageRequestParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("save", c_uint8)]

class UseExternalI2cSpiUartGpioVoltageRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t),
                ("parameters", UseExternalI2cSpiUartGpioVoltageRequestParameters_t)]

UseExternalI2cSpiUartGpioVoltageRequestArray_t = c_uint8 * sizeof(UseExternalI2cSpiUartGpioVoltageRequestFields_t)

class UseExternalI2cSpiUartGpioVoltageRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", UseExternalI2cSpiUartGpioVoltageRequestArray_t),
                ("fields", UseExternalI2cSpiUartGpioVoltageRequestFields_t)]

# Response --------------------------------------------------------------------- #

class UseExternalI2cSpiUartGpioVoltageResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("voltage_mV", c_uint16)]

class UseExternalI2cSpiUartGpioVoltageResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", UseExternalI2cSpiUartGpioVoltageResponseParameters_t)]

UseExternalI2cSpiUartGpioVoltageResponseArray_t = c_uint8 * sizeof(UseExternalI2cSpiUartGpioVoltageResponseFields_t)

class UseExternalI2cSpiUartGpioVoltageResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", UseExternalI2cSpiUartGpioVoltageResponseArray_t),
                ("fields", UseExternalI2cSpiUartGpioVoltageResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a buffer object
        """
        self.data = UseExternalI2cSpiUartGpioVoltageResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result],
            "voltage_mV": self.fields.parameters.voltage_mV
        }

# endregion

#================================================================================#
# region GET ANALOG MEASUREMENTS
#================================================================================#

# Request ---------------------------------------------------------------------- #

class GetAnalogMeasurementsRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

GetAnalogMeasurementsRequestArray_t = c_uint8 * sizeof(GetAnalogMeasurementsRequestFields_t)

class GetAnalogMeasurementsRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GetAnalogMeasurementsRequestArray_t),
                ("fields", GetAnalogMeasurementsRequestFields_t)]

# Response --------------------------------------------------------------------- #

class GetAnalogMeasurementsResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("vmeasVtargI2cSpiUartGpio_mV", c_uint16),
                ("vmeasVtargI3cHV_mV", c_uint16),
                ("vmeasVtargI3cLV_mV", c_uint16),
                ("vmeasVcca_mV", c_uint16),
                ("vmeasVccaI3c_mV", c_uint16),
                ("vmeasVddio2_mV", c_uint16)]

class GetAnalogMeasurementsResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", GetAnalogMeasurementsResponseParameters_t)]

GetAnalogMeasurementsResponseArray_t = c_uint8 * sizeof(GetAnalogMeasurementsResponseFields_t)

class GetAnalogMeasurementsResponse_t(BaseCommandResponse_t):

    _fields_ = [("data", GetAnalogMeasurementsResponseArray_t),
                ("fields", GetAnalogMeasurementsResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a buffer object
        """
        self.data = GetAnalogMeasurementsResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result],
            "i2c_spi_uart_gpio_vtarg": {
                "internal_mV": self.fields.parameters.vmeasVcca_mV,
                "external_mV": self.fields.parameters.vmeasVtargI2cSpiUartGpio_mV,
            },
            "i3c_low_voltage_vtarg": {
                "internal_mV": self.fields.parameters.vmeasVccaI3c_mV,
                "external_mV": self.fields.parameters.vmeasVtargI3cLV_mV,
            },
            "i3c_high_voltage_vtarg": {
                "internal_mV": self.fields.parameters.vmeasVddio2_mV,
                "external_mV": self.fields.parameters.vmeasVtargI3cHV_mV,
            }
        }

# endregion

#================================================================================#
# region GET I3C CONNECTORS STATUS
#================================================================================#

class I3cConnectorPort_t(Enum):
    I3C_LOW_VOLTAGE_PORT   = 0x00
    I3C_HIGH_VOLTAGE_PORT  = 0x01

class I3cConnectorEvent_t(Enum):
    I3C_CONNECTOR_PLUGGED       = 0x00
    I3C_CONNECTOR_UNPLUGGED     = 0x01

class I3cConnectorType_t(Enum):
    CONNECTOR_IDENTIFICATION_NOT_SUPPORTED  = 0x00
    I3C_HARNESS                             = 0x01
    QWIIC_ADAPTER                           = 0x02
    SENSEPEEK_PROBES                        = 0x03
    NO_CONNECTOR                            = 0x04
    ERROR_IDENTIFYING_CONNECTOR             = 0x05

# Request ---------------------------------------------------------------------- #

# Union structure
class GetI3cConnectorsStatusRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

GetI3cConnectorsStatusRequestArray_t = c_uint8 * sizeof(GetI3cConnectorsStatusRequestFields_t)

class GetI3cConnectorsStatusRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GetI3cConnectorsStatusRequestArray_t),
                ("fields", GetI3cConnectorsStatusRequestFields_t)]

# Response --------------------------------------------------------------------- #

class GetI3cConnectorsStatusResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("lvConnectorStatus", c_uint8),     # The connectorStatus field gives support for the Rev. B since It doesn't have connector identification
                ("lvConnectorType", c_uint8),
                ("hvConnectorStatus", c_uint8),
                ("hvConnectorType", c_uint8)]

class GetI3cConnectorsStatusResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", GetI3cConnectorsStatusResponseParameters_t)]

GetI3cConnectorsStatusResponseArray_t = c_uint8 * sizeof(GetI3cConnectorsStatusResponseFields_t)

class GetI3cConnectorsStatusResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", GetI3cConnectorsStatusResponseArray_t),
                ("fields", GetI3cConnectorsStatusResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a buffer object
        """
        self.data = GetI3cConnectorsStatusResponseArray_t.from_buffer_copy(data)

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result],
            "i3c_low_voltage_port": {
                "state": I3cConnectorEvent_t(self.fields.parameters.lvConnectorStatus).name,
                "connector_type": I3cConnectorType_t(self.fields.parameters.lvConnectorType).name
            },
            "i3c_high_voltage_port": {
                "state": I3cConnectorEvent_t(self.fields.parameters.hvConnectorStatus).name,
                "connector_type": I3cConnectorType_t(self.fields.parameters.hvConnectorType).name
            }
        }

# endregion

#================================================================================#
# region GET DEVICE INFO
#================================================================================#

# Request ---------------------------------------------------------------------- #
class GetDeviceInfoRequestFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandRequestHeader_t)]

GetDeviceInfoRequestArray_t = c_uint8 * sizeof(GetDeviceInfoRequestFields_t)

class GetDeviceInfoRequest_t(BaseCommandRequest_t):
    _fields_ = [("data", GetDeviceInfoRequestArray_t),
                ("fields", GetDeviceInfoRequestFields_t)]
    
# Response --------------------------------------------------------------------- #

class DeviceManufacturer_t(Enum):
    Binho_LLC = 0x00

class ProductName_t(Enum):
    Supernova = 0x00
    Pulsar = 0x01

MANUFACTURER_INDEX  = 0
PRODUCT_NAME_INDEX  = 1
HW_VERSION_INDEX    = 2
SERIAL_NUMBER_INDEX = 3
SERIAL_NUMBER_SIZE  = 32
FW_VERSION_INDEX    = SERIAL_NUMBER_INDEX + SERIAL_NUMBER_SIZE

GET_DEVICE_INFO_PAYLOAD_LENGTH = 73

class GetDeviceInfoResponseParameters_t(Structure):
    _pack_ = 1
    _fields_ = [("firmwareVersionLength", c_uint8),
                ("payloadLength", c_uint8)]

GetDeviceInfoResponsePayload_t = c_uint8 * GET_DEVICE_INFO_PAYLOAD_LENGTH

class GetDeviceInfoResponseFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", CommandResponseHeader_t),
                ("parameters", GetDeviceInfoResponseParameters_t),
                ("payload", GetDeviceInfoResponsePayload_t)]
    
GetDeviceInfoResponseArray_t = c_uint8 * sizeof(GetDeviceInfoResponseFields_t)

class GetDeviceInfoResponse_t(BaseCommandResponse_t):
    _fields_ = [("data", GetDeviceInfoResponseArray_t),
                ("fields", GetDeviceInfoResponseFields_t)]

    def fromBytes(self, data):
        """
        This function set the ctypes Array data from a buffer object
        """
        for i in range(len(data)):
            self.data[i] = data[i]

    def toDictionary(self) -> dict:

        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result],
            "manufacturer": DeviceManufacturer_t(self.fields.payload[MANUFACTURER_INDEX]).name.replace("_", " "),
            "product_name": ProductName_t(self.fields.payload[PRODUCT_NAME_INDEX]).name.replace("_", " "),
            "serial_number": bytes(self.fields.payload[SERIAL_NUMBER_INDEX:SERIAL_NUMBER_INDEX + SERIAL_NUMBER_SIZE]).decode('ascii'),
            "hardware_version": bytes([self.fields.payload[HW_VERSION_INDEX]]).decode('ascii'),
            "firmware_version": bytes(self.fields.payload[FW_VERSION_INDEX:FW_VERSION_INDEX + self.fields.parameters.firmwareVersionLength]).decode('ascii'),
            "capabilities": {"supported_groups": [Group(group).name for group in self.fields.payload[FW_VERSION_INDEX + self.fields.parameters.firmwareVersionLength:self.fields.parameters.payloadLength]]}
        }

# endregion

#================================================================================#
# region I3C CONNECTOR NOTIFICATION
#================================================================================#

class I3cConnectorNotificationParametersFields_t(Structure):
    _pack_ = 1
    _fields_ = [("port", c_uint8),
                ("event", c_uint8),
                ("connectorType", c_uint8)]

class I3cConnectorNotificationFields_t(Structure):
    _pack_ = 1
    _fields_ = [("header", NotificationHeader_t),
                ("parameters", I3cConnectorNotificationParametersFields_t)]

I3cConnectorNotificationArray_t = c_uint8 * sizeof(I3cConnectorNotificationFields_t)

class I3cConnectorNotification_t(Union):
    _fields_ = [("data", I3cConnectorNotificationArray_t),
                ("fields", I3cConnectorNotificationFields_t)]

    def toDictionary(self) -> dict:
        return {
            "id": self.fields.header.id,
            "command": SYS_COMMAND_NAMES[self.fields.header.code],
            "result": SYS_RESULT_NAMES[self.fields.header.result],
            "event": I3cConnectorEvent_t(self.fields.parameters.event).name,
            "port": I3cConnectorPort_t(self.fields.parameters.port).name,
            "connector_type": I3cConnectorType_t(self.fields.parameters.connectorType).name
        }

    def __str__(self) -> str:
        return str(self.toDictionary())

# endregion