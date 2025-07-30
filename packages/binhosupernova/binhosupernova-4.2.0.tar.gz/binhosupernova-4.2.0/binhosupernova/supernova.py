"""
Binho Supernova Python package

This Python package is developed to control the new Supernova USB Host adapter.
The new Binho Supernova device is an USB HID device that is controlled using a set
of USB commands that are transferred over USB HID Interrupt transfers.
"""
from .usb.usb_hid_manager import UsbHidManager, SUPERNOVA_PID, USB_TRANSFER_ERROR_OPCODE

# Import commands libraries.
from .commands.system.validators import *
from .commands.i2c.validators import *
from .commands.i3c.validators import *
from .commands.spi.validators import *
from .commands.uart.validators import *
from .commands.gpio.validators import *

# Import other modules
from .utils.system_message import *
import inspect
import functools

class Supernova:
    """
    This class represents the Binho Supernova device and provides the methods to take full control of it.
    It is composed of an instance of the UsbHidManager, which is in charge of the USB communication
    with the USB Host Adapter and the onEventCallback which is a callback function that must be defined and
    registered by the API client. This callback allows the API to return command responses and asynchronous
    notification sent by the device, or report an unexpected disconnection of the device without calling the
    close() method as a system message. See the documentation of the onEvent method to get more information.

    Attributes
    ----------
    usbHidManager: UsbHidManager
        Instance of the UsbHidManager class in charge of controlling the communication of the USB Host
        Adapter over USB HID.
    
    responsesMap: dict
        A Python dictionary that acts as a map to match requests' id with the response instance.
    
    onEventCallback
        Callback invoked to return Supernova's responses and notifications.

    """

    # Private method ----------------------------------------------------------------------------------

    def __sendMessage(self, request_metadata, result) -> None:
        """
        This method is used to send a new message via USB. The method register the response instance with
        the transaction id in the responses map, and sends all the needed packages via USB to the Supernova.
        
        Parameters
        ---------
        request_metadata: dict
            A python dictionary containing the request id, the request serialization to be sent to 
            the Supernova, and the response instance to be saved in the responsesMap dictionary
            together with the id.
        
        result: SystemMessage
            A SystemMessage instance that will be returned to the user application.
        """
        self.responsesMap[request_metadata["id"]] = request_metadata["response"]
        # Send message to the Supernova
        transfer_result = self.usbHidManager.send(request_metadata["request"])
        if transfer_result == USB_TRANSFER_ERROR_OPCODE:
            result.module = SystemModules.SYSTEM
            result.opcode = SystemOpcode.USB_COMMUNICATION_ERROR
            result.message = "USB communication error. Please check the connection and try again."

    def __checkConnection(func):
        """
        Decorator used to verify that the Supernova is correctly configured before using its functionalities
        """
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if not(self.usbHidManager.isRunning()):
                sys_response = SystemMessage(SystemModules.SYSTEM, SystemOpcode.CONFIGURATION_ERROR, "Supernova not configured appropriately, please check if connection is open and callback is set")
                return sys_response.toDictionary()
            return func(self, *args, **kwargs)
        return wrapper

    def __onReceiveDriverCallback(self, supernova_response, system_message):
        """
        This function is a built-in callback to be set by default, which is invoked by the usbHidManager
        attribute when a new message sent by the USB host adapter is received, or by all the different parts
        of the system, including the usbHidManager attribute when an unexpected event occurs. If a new message
        from the USB host is received, it identifies the type of message whether it is a command response or
        an asynchronous notification. If it is a command response, it looks up the response instance from the
        responsesMap attribute by the command id. Otherwise, invokes the notification constructor based on the
        notification code. Finally, it calls the user-defined callback if it was previously defined and
        registered by the client of the API. In case of an unexpected disconnection, the usbHidManager will
        return a SystemMessage indicating the unexpected disconnection.

        Parameters
        ---------
        supernova_response: bytes
            A bytes object containing the stream of bytes sent by the Supernova
        
        system_message: dict
            A dictionary representation of a SystemMessage instance.
        
        """

        if supernova_response:

            # Get command id to search the response in the transfers map.
            id = (supernova_response[ID_LSB_INDEX] | supernova_response[ID_MSB_INDEX] << 8)

            # Look for the receiver of the message.
            command = (supernova_response[COMMAND_CODE_LSB_INDEX] | supernova_response[COMMAND_CODE_MSB_INDEX] << 8)

            # Check if the message from the USB Host Adapter corresponds to a request from the USB Host.
            if getCommandType(command) == CommandType.REQUEST_RESPONSE.value:

                # Get response from response map with the id.
                response = self.responsesMap.get(id)

                if response is not None:
                    response.fromBytes(supernova_response)
                    # Invoke callback
                    if self.onEventCallback:
                        self.onEventCallback(response.toDictionary(), None)
                    self.responsesMap.pop(id, None)
                else:
                    # TODO: Raise an Unexpected response exception or similar.
                    pass

            # If the message is a notification
            elif getCommandType(command) == CommandType.NOTIFICATION.value:

                # Identify what notification it is.
                if command == I3cCommandCodes.I3C_CONTROLLER_IBI_REQUEST_NOTIFICATION.value:
                    notification = I3cControllerIbiRequestNotification_t.from_buffer_copy(supernova_response)

                elif command == I3cCommandCodes.I3C_CONTROLLER_HJ_REQUEST_NOTIFICATION.value:
                    notification = I3cControllerHotJoinRequestNotification_t.from_buffer_copy(supernova_response)

                # Check if it's an I3C Target notification
                elif command == I3cCommandCodes.I3C_TARGET_BUS_EVENT_NOTIFICATION.value:
                    notification = I3cTargetBusEventNotification_t()
                    notification.fromBytes(supernova_response)

                # Check if it's a UART read notification
                elif command == UartCommandCodes.UART_RECEIVE_NOTIFICATION.value:
                    notification = UartReceiveNotification_t()
                    notification.fromBytes(supernova_response)

                # Check if it's an I3C Connector notification
                elif command == SysCommandCodes.SYS_I3C_CONNECTOR_EVENT_NOTIFICATION.value:
                    notification = I3cConnectorNotification_t.from_buffer_copy(supernova_response)

                # Check if it's a GPIO interrupt notification
                elif command == GpioCommandCodes.GPIO_INTERRUPT_NOTIFICATION.value:
                    notification = GpioInterruptNotification_t.from_buffer_copy(supernova_response)

                if self.onEventCallback:
                        self.onEventCallback(notification.toDictionary(), None)

        if system_message:
            #Send system message to application.
            if self.onEventCallback:
                self.onEventCallback(None,system_message)

    def __init__(self):
        """
        Constructor defined to add the Supernova attributes and initialize them.
        """
        # HID device used to connect to the supernova via USB
        self.usbHidManager = UsbHidManager(SUPERNOVA_PID)
        self.usbHidManager.setOnReceiveCallback(self.__onReceiveDriverCallback)

        # Responses handling
        self.responsesMap = {}                  # Request id - Response instance map
        self.onEventCallback = None

    # Public methods ----------------------------------------------------------------------------------

    def open(self, serial = None, path:str = None) -> dict:
        """
        This method establishes the USB communication with the Supernova. When this method is invoked, the
        USB Host starts to send USB frames to the USB device, and to pole the Input endpoint.

        By default, the USB hid manager, opened connection with the first Supernova listed based on the
        VID and PID. Optionally, the serial number or the OS path string can be used to identify the
        device, so passing the serial number or the path only is enough to connect with the desired device.

        To get the device path or serial number, the BinhoSupernova.getConnectedSupernovaDevicesList() method
        can be invoked.

        Parameters
        ----------
        serial : int
            USB device serial number. By default is None.
        
        path : str
            String path generated by the OS that can be read using the BinhoSupernova.getConnectedSupernovaDevicesList() method.

        Returns
        -------
        dict:
            A python dictionary representation of a SystemMessage instance. The opcode of the message is:
            - SystemOpcode.OK if the connection with the HID device is completed successfully.
            - SystemOpcode.OPEN_CONNECTION_FAIL if the connection of the HID instance fails.

        """
        return self.usbHidManager.open(serial, path)

    def close(self) -> dict:
        """
        This method closes the communication with the Supernova and releases the used memory.
        
        Returns
        -------
        dict:
            A python dictionary representation of a SystemMessage instance. The opcode of the message is:
            - SystemOpcode.OK if the connection with the HID device is closed successfully.
            - SystemOpcode.OPEN_CONNECTION_REQUIRED if the was not previously opened.

        """
        return self.usbHidManager.close()

    def onEvent(self, callback_func) -> dict:
        """
        This method registers the callback invoked every time a new USB response or notification
        arrives from the USB device. The callback function must implement the following signature:

            def callback(supernova_response, system_message) -> None:

        The parameter supernova_response corresponds to a new message sent by the USB device as a
        response to a command or an asynchronous notification. The parameter system_message corresponds
        to a SystemMessage instance that contains information about the Supernova's status. When an
        unexpected disconnection of the device occurs, the system_message parameter will contain a
        SystemMessage indicating the unexpected disconnection.

        It's important to note that the callback is called directly from the built-in callback 
        onReceiveCallback. If the callback function introduces a delay, it can impact the receiving 
        mechanism. Developers using this SDK are advised to implement a queuing mechanism to quickly
        liberate the SDK as soon as the callback is called. This approach helps in managing 
        responses efficiently without blocking the SDK's processing capabilities.

        Parameters
        ----------
        callback_func: function
            Callback function that will be invoked every time a new USB response or notification is
            sent by the USB device.

        Returns
        -------
        dict
            The SystemMessage in dictionary format.

        """

        sys_response = SystemMessage(SystemModules.SYSTEM, SystemOpcode.OK, "On event callback function registered successfully.")

        # Get the function signature
        func_signature = inspect.signature(callback_func)

        # Get the parameters of the function
        func_parameters = func_signature.parameters

        # Check if the function has exactly 2 parameters
        if len(func_parameters) != 2:
            sys_response.opcode = SystemOpcode.INVALID_CALLBACK_SIGNATURE
            sys_response.message = "The function must accept 2 Parameters: callback(supernova_response, system_message)."
        else:
            # Save the callback function
            self.onEventCallback = callback_func

        return sys_response.toDictionary()

    # -----------------------------------------------------------------------------------
    # Communication API - USB commands
    # -----------------------------------------------------------------------------------

    # Get USB strings -------------------------------------------------------------------
    @__checkConnection
    def getUsbString(self, id: int, subCommand : GetUsbStringSubCommand) -> dict:

        """
        This function sends a Get USB String command taking the subcommand
        passed as parameter. The list of subcommands:

        GetUsbStringSubCommand.MANUFACTURER - Returns the manufacturer string ("Binho").
        GetUsbStringSubCommand.PRODUCT_NAME - Returns the product name string ("Binho Supernova").
        GetUsbStringSubCommand.SERIAL_NUMBER - Returns the product serial number. Up to 32 characters.
        GetUsbStringSubCommand.FW_VERSION - Returns the product firmware version (VX.X.X).
        GetUsbStringSubCommand.HW_VERSION - Returns the product hardware version (HW-X).
        GetUsbStringSubCommand.BT_VERSION - Returns the product bootloader version (VX.X.X).

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The range allowed is [1, 65535].

        subCommand : GetUsbStringSubCommand
            Subcommand that indicates what string must be retrieved.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "subcommand" : subCommand
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = getUsbStringValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response 
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()
    
    # Get Device Info ---------------------------------------------------------------------------
    @__checkConnection
    def getDeviceInfo(self, id: int) -> dict:
        """
        This function sends a GET_DEVICE_INFO command to the device. The device returns a dictionary
        with its information.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = getDeviceInfoValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response 
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    # Set I3C Voltage strings -------------------------------------------------------------------
    @__checkConnection
    def setI3cVoltage(self, id: int, voltage_mV : c_uint16) -> dict:
        """
        This function sends a SET_I3C_VOLTAGE command taking desired LDO output voltage (in mV) as parameter.
        
        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        voltage_mV : c_uint16   
            This voltage determines two function modes:
            1 - I3C_LOW_VOLTAGE_MODE that allows voltages in the range [800, 1200) mV
            2 - I3C_STANDARD_VOLTAGE_MODE that allows voltages in the range [1200, 3300] mV

            The value 0 mV is allowed to power off the output voltage.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.  
        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "voltage_mV" : voltage_mV
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = setI3cVoltageValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response 
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def resetDevice(self, id: int) -> dict:
        """
        This function sends a RESET DEVICE command.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.  
        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = resetDeviceValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response 
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Wait for the usb manager to end.
        self.usbHidManager.join()

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def enterBootMode(self, id: int) -> dict:
        """
        This function sends a ENTER BOOT MODE command.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.  
        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = enterBootModeValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response 
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Wait for the usb manager to end.
        self.usbHidManager.join()

        # Return result in dict format.
        return result.toDictionary()


    @__checkConnection
    def enterIspMode(self, id: int) -> dict:
        """
        This method sends a ENTER_ISP_MODE command

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = enterIspModeValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Wait for the usb manager to end.
        self.usbHidManager.join()

        # Return result in dict format.
        return result.toDictionary()

    # Set I2C SPI UART GPIO Voltage strings -------------------------------------------------------------------

    @__checkConnection
    def setI2cSpiUartGpioVoltage(self, id: int, voltage_mV : c_uint16, save: bool = False) -> dict:
        """
        This method sends a SET_I2C_SPI_UART_GPIO_VOLTAGE command taking desired bus voltage

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        voltage_mV : c_uint16
            It is a 2-bytes integer that indicates the I2C, SPI, UART and GPIO operating voltage. The allowed range is [1200, 3300] mV
            and the value 0 mV to power off the output voltage.

        save : bool
            It indicates if the bus voltage configuration must be stored in the device non-volatile memory.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "voltage_mV" : voltage_mV,
            "save" : save
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = setI2cSpiUartGpioVoltValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def getI3cConnectorsStatus(self, id: int) -> dict:
        """
        This method sends a GET_I3C_CONNECTORS_STATUS command and retrieves the actual state of the I3C Connectors Ports.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = getI3cConnectorsStatusValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def getAnalogMeasurements(self, id: int) -> dict:
        """
        This method sends a GET_ANALOG_MEASUREMENTS command and retrieves the analog measures in mV.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = getAnalogMeasurementsValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def useExternalI2cSpiUartGpioVoltage(self, id: int, save: bool = False) -> dict:
        """
        This method sends a USE_EXT_SRC_I2C_SPI_UART_GPIO_VOLTAGE command, sets the bus voltage to a measured value and
        retrieves the analog signal measure in mV.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        save : bool
            It indicates if the bus voltage configuration must be stored in the device non-volatile memory.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "save" : save
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = useExternalI2cSpiUartGpioVoltageValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def useExternalI3cVoltage(self, id: int) -> dict:
        """
        This method sends a USE_EXT_SRC_I3C_BUS_VOLTAGE command, sets the bus voltage to a measured value and
        retrieves the analog signal measure in mV.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = useExternalI3cVoltageValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    # I2C management --------------------------------------------------------------------
    
    @__checkConnection
    def i2cControllerInit(self, id: int, frequency: int, pullUpResistorsValue: I2cPullUpResistorsValue) -> dict:
        """
        This method initialize the I2C bus in controller mode with
        the frequency and pull up resistors value selected.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The range allowed is [1, 65535].

        frequency : int
            This parameter represents the I2C SCL frequency in Hz. Currently, the minimum allowed value
            is 100000 Hz and the maximum allowed value is 1000000 Hz.

        pullUpResistorsValue : I2cPullUpResistorsValue
            Value of the pull up enum that represents the desired Pull Up resistors value

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "busId" : I2cBus.I2C_BUS_A,
            "frequency_Hz" : frequency,
            "pullUpValue" : pullUpResistorsValue
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i2cControllerInitValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i2cControllerSetParameters(self, id: int, frequency: int, pullUpResistorsValue: I2cPullUpResistorsValue) -> dict:
        """
        This method sets the I2C transfers baudrate and pull up resistors value for the SDA and SCL lines.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The range allowed is [1, 65535].

        frequency : int
            This parameter represents the I2C SCL frequency in Hz. Currently, the minimum allowed value
            is 100000 Hz and the maximum allowed value is 1000000 Hz.
        
        pullUpResistorsValue : I2cPullUpResistorsValue
            Value of the pull up enum that represents the desired Pull Up resistors value

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "busId" : I2cBus.I2C_BUS_A,
            "frequency_Hz" : frequency,
            "pullUpValue" : pullUpResistorsValue
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i2cControllerSetParametersValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i2cSetPullUpResistors(self, id: int, pullUpResistorsValue: I2cPullUpResistorsValue) -> dict:
        """
        This method sets the I2C pull up resistors for the SDA and SCL lines.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The range allowed is [1, 65535].

        pullUpResistorsValue : I2cPullUpResistorsValue Enum
            This parameter represents the different values for the pull up resistors.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "busId" : I2cBus.I2C_BUS_A,
            "pullUpResistorsValue" : pullUpResistorsValue
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i2cSetPullUpResistorsValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i2cControllerWrite(self, id: int, targetAddress : int, registerAddress: list, data: list, isNonStop: bool = False, is10BitTargetAddress: bool = False) -> dict:
        """
        This method is used to request to the the Supernova device to perform an I2C write transfer. The
        I2C write transfer starts with a START condition and ends with a STOP condition. To perform a write
        transfer without the STOP condition, the nonStop parameter must be set to True.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        targetAddress : byte
            I2C slave static address.

        registerAddress : list
            Python list that contains the memory/register address of the I2C slave internal memory, whose data
            will be written. The list holds bytes, and can hand hold from 0 bytes up to 4 bytes. 0 bytes means
            that the list can be left empty and the Supernova will ignore it and write only the data payload.

        data : list
            Python list that contains the I2C data transferred in the I2C Write transfer. The list holds
            bytes elements, and the maximum length is 1024 bytes.
        
        isNonStop : bool
            This parameter indicates if the I2C write transfer is non-stop, meaning that it ends without a STOP 
            condition. If the flag is set to False, the transfer ends with STOP; otherwise, if it's True, the 
            transfer is non-stop, without a STOP condition at the end.

        is10BitTargetAddress : bool
            This parameter indicates if the target address is a 10-bit address. If the flag is set to False, the
            target address is a 7-bit address; otherwise, if it's True, the target address is a 10-bit address.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "busId" : I2cBus.I2C_BUS_A,
            "targetAddress" : targetAddress,
            "is10BitTargetAddress" : is10BitTargetAddress,
            "registerAddress" : registerAddress,
            "data" : data,
            "isNonStop" : isNonStop
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i2cControllerWriteValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i2cControllerRead(self, id: int, targetAddress: int, requestDataLength: int, registerAddress: list = [], is10BitTargetAddress: bool = False) -> dict:
        """
        This method is used to request to the the USB device to perform an I2C read transfer. The
        I2C read transfer starts with a START condition and ends with a STOP condition.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        targetAddress : byte
            I2C target static address.

        requestDataLength : int
            Length of the read data. The maximum value is 1024 bytes.
        
        registerAddress : list
            Python list that contains the memory/register address of the I2C target internal memory, whose data
            will be read. The list holds bytes, and can hand hold from 0 bytes up to 4 bytes. 0 bytes means
            that the list can be left empty, the Supernova will ignore it and will perform only a read transfer.

        is10BitTargetAddress : bool
            This parameter indicates if the target address is a 10-bit address. If the flag is set to False, the
            target address is a 7-bit address; otherwise, if it's True, the target address is a 10-bit address.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "busId" : I2cBus.I2C_BUS_A,
            "targetAddress" : targetAddress,
            "is10BitTargetAddress" : is10BitTargetAddress,
            "registerAddress" : registerAddress,
            "dataLength" : requestDataLength
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i2cControllerReadValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()
    
    @__checkConnection
    def i2cControllerScanBus(self, id: int, include10BitAddresses: bool = False) -> dict:
        """
        This method is used to request to the the USB device to perform an I2C scan of the I2C bus.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].
        
        include10BitAddresses : bool
            This parameter indicates if the scan must include 10-bit addresses. If the flag is set to False, the
            scan will not include 10-bit addresses; otherwise, if it's True, the scan will include 10-bit addresses.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "busId" : I2cBus.I2C_BUS_A,
            "include10BitAddresses" : include10BitAddresses,
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i2cControllerScanBusValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    # I3C management --------------------------------------------------------------------

    @__checkConnection
    def i3cControllerInit(self, id: c_uint16, pushPullRate: I3cPushPullTransferRate, i3cOpenDrainRate: I3cOpenDrainTransferRate, i2cOpenDrainRate: I2cTransferRate, driveStrength: I3cDriveStrength = I3cDriveStrength.FAST_MODE) -> dict:
        """
        This function is in charge of initializing the I3C peripheral of the Supernova as a controller.

        Parameters
        ----------
        id : c_uint16
                An integer number that identifies the transfer.

        pushPullRate : I3cPushPullTransferRate
            The push-pull rate for I3C transfers

        i3cOpenDrainRate : I3cOpenDrainTransferRate
            The open-drain rate for I3C transfers

        i2cOpenDrainRate : I2cTransferRate
            The open-drain rate for I2C transfers

        driveStrength : I3cDriveStrength
            The drive strength for I3C pins. Optional parameter, with default value Fast mode

        Returns
        -------
        dict:
            dictionary that indicates the result of the validation of the data
        """

        metadata = {
            "id" : id,
            "pushPullRate" : pushPullRate,
            "i3cOpenDrainRate" : i3cOpenDrainRate,
            "i2cOpenDrainRate" : i2cOpenDrainRate,
            "driveStrength" : driveStrength
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerInitValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerSetParameters(self, id: c_uint16, pushPullRate: I3cPushPullTransferRate, i3cOpenDrainRate: I3cOpenDrainTransferRate, i2cOpenDrainRate: I2cTransferRate, driveStrength: I3cDriveStrength = I3cDriveStrength.FAST_MODE) -> dict:
        """
        Request the I3C CONTROLLER SET PARAMETERS command in order to set the different SCL frequencies.

        Parameters
        ----------
        id : c_uint16
            An integer number that identifies the transfer.

        pushPullRate : I3cPushPullTransferRate
            The push-pull rate for I3C transfers

        i3cOpenDrainRate : I3cOpenDrainTransferRate
            The open-drain rate for I3C transfers

        i2cOpenDrainRate : I2cTransferRate
            The open-drain rate for I2C transfers

        driveStrength : I3cDriveStrength
            The drive strength for I3C pins. Optional parameter, with default value Fast mode

        Returns
        -------
        dict:
            dictionary that indicates the result of the validation of the data
        """

        metadata = {
            "id" : id,
            "pushPullRate" : pushPullRate,
            "i3cOpenDrainRate" : i3cOpenDrainRate,
            "i2cOpenDrainRate" : i2cOpenDrainRate,
            "driveStrength" : driveStrength
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerSetParametersValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerInitBus(self, id: int, targetDeviceTable: dict = None) -> dict:
        """
        This method is used to Initialize the I3C bus for communication with I3C devices.

        Parameters
        ----------
        id : int
            A 2-byte integer representing the initialization ID. The range allowed is [1, 65535].

        targetDeviceTable : dict, optional
            A dictionary containing information about the target devices connected to the I3C bus.
            The default value is None.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        metadata = {
            "id" : id,
            "targetDeviceTable" : targetDeviceTable
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerInitBusValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerResetBus(self, id: c_uint16) -> dict:
        """
        Request the I3C CONTROLLER RESET BUS command.

        Parameters
        ----------
        id : c_uint16
            An integer number that identifies the transfer.

        Returns
        -------
        dict:
            dictionary that indicates the result of the validation of the data
        """

        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerResetBusValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerGetTargetDevicesTable(self, id: int) -> dict:
        """
        This method retrieves the target device table information from the I3C bus.
        The retrieved PID for each target is in MSB order.

        Parameters
        ----------
        id : int
            A 2-byte integer representing the request ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        metadata = {
            "id" : id
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerGetTargetDevicesTableValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerSetTargetDeviceConfiguration(self, id: int, targetAddress: c_uint8, configuration: dict) -> dict:
        """
        This method changes de configuration of an I3C target given by a dictionary containing
        the target configuration.

        Parameters
        ----------
        id : int
            A 2-byte integer representing the request ID. The range allowed is [1, 65535].

        targetAddress: c_uint8
            Target address whose configuration will be set.

        configuration : dict
            A dictionary containing the new configuration.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "targetAddress": targetAddress,
            "configuration" : configuration
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerSetTargetDeviceConfigurationValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerWrite(self, id: c_uint16, targetAddress: c_uint8, mode: TransferMode, registerAddress: list, data: list, startWith7E: bool = True) -> dict:
        """
        This method is used to request to the Supernova device to perform an I3C write transfer. The
        I3C write transfer starts with a START condition and ends with a STOP condition.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device for writing data.

        mode : TransferMode
            The transfer mode for the write operation.

        registerAddress : list
            A list containing the memory/register address of the I3C target internal memory
            from which data will be written. It can hold from 0 to 4 bytes.

        data : list
            A list containing the data to be written to the device.

        startWith7E: bool
            Boolean flag to indicate if the transfer must start with the broadcast address 0x7E.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "targetAddress" : targetAddress,
            "mode" : mode,
            "registerAddress" : registerAddress,
            "data" : data,
            "startWith7E": startWith7E
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerWriteValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerRead(self, id: c_uint16, targetAddress: c_uint8, mode: TransferMode ,registerAddress: list, length: c_uint16, startWith7E: bool = True) -> dict:
        """
        This method is used to request to the USB device to perform an I3C read transfer. The
        I3C read transfer starts with a START condition and ends with a STOP condition.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which data will be read.

        mode : TransferMode
            The transfer mode for the read operation.

        registerAddress : list
            A list containing the memory/register address of the I3C target internal memory
            from which data will be read. It can hold from 0 to 4 bytes.

        length : c_uint16
            The length of the data to be read.

        startWith7E: bool
            Boolean flag to indicate if the transfer must start with the broadcast address 0x7E.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "targetAddress" : targetAddress,
            "mode" : mode,
            "registerAddress" : registerAddress,
            "length" : length,
            "startWith7E": startWith7E
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerReadValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerCccTransfer(self, id: c_uint16, cmdType: c_uint8, direction: TransferDirection, targetAddress: c_uint8, mode: TransferMode, defByte: c_uint8, ccc: c_uint8, length: c_uint16, data: list) -> dict:
        """
        This method is used to send CCCs on the Supernova, it is wrapped by the specific CCCs to change its functionality.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which data will be read.

        mode : TransferMode
            The transfer mode for the read operation.

        registerAddress : list
            A list containing the memory/register address of the I3C target internal memory
            from which data will be read. It can hold from 0 to 4 bytes.

        length : c_uint16
            The length of the data to be read.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "commandType" : cmdType,
            "direction" : direction,
            "targetAddress" : targetAddress,
            "mode" : mode,
            "defByte" : defByte,
            "ccc" : ccc,
            "length" : length,
            "data" : data
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerCccTransferValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerTriggerTargetResetPattern(self, id: c_uint16) -> dict:
        """
        This method triggers an I3C Target Reset Pattern on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "pattern" : I3cPattern.I3C_TARGET_RESET_PATTERN
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerTriggerPatternValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerTriggerHdrExitPattern(self, id: c_uint16) -> dict:
        """
        This method triggers an I3C Exit Pattern on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "pattern" : I3cPattern.I3C_HDR_EXIT_PATTERN
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerTriggerPatternValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerHdrDdrWrite(self, id: c_uint16, targetAddress: c_uint8, command: c_uint8, data: list) -> dict:
        """
        This method is used to request to the Supernova device to perform an I3C write transfer in HDR-DDR mode. If the bus is in
        I3C SDR mode, automatically starts emitting the ENTHDR0 CCC.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device for writing data.

        command : c_uint8
            The HDR-DDR command in the range [0x00, 0x7F].

        data : list
            A list containing the data to be written to the device. The length of this list must be a multiple of 2.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "targetAddress" : targetAddress,
            "command" : command,
            "data" : data
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerHdrDdrWriteValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cControllerHdrDdrRead(self, id: c_uint16, targetAddress: c_uint8, command: c_uint8, length: c_uint16) -> dict:
        """
        This method is used to request to the Supernova device to perform an I3C write transfer in HDR-DDR mode. If the bus is in
        I3C SDR mode, automatically starts emitting the ENTHDR0 CCC.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device for writing data.

        command : c_uint8
            The HDR-DDR command in the range [0x80, 0xFF].

        length : c_uint16
            The length of the data to be read. The length must be multiple of 2.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "targetAddress" : targetAddress,
            "command" : command,
            "length" : length
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cControllerHdrDdrReadValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cTargetInit(self, id: c_uint16, memoryLayout: I3cTargetMemoryLayout_t, pid: list, bcr: c_uint8, dcr: c_uint8, staticAddress: c_uint8, mwl: c_uint16 = 1024, mrl: c_uint16 = 1024) -> dict:
        """
        This function is in charge of initializing the I3C peripheral of the Supernova as a target.

        Parameters
        ----------
        id : c_uint16
             An integer number that identifies the transfer.

        memoryLayout: I3cTargetMemoryLayout_t
            Layout of the memory that the target represents.

        pid: list
            List of 6 bytes that represents the 48-bit Provisioned ID (PID).

        bcr: c_uint8
            Bus Characteristics Register.

        dcr: I3cTargetDcr_t
            Device Characteristics Register. Determines the type of device the Supernova represents.
            The enum I3cTargetDcr_t provides 3 predefined DCR values.

        staticAddress: c_uint8
            I2C static address of the Supernova.

        mwl: c_uint16
            Maximum write length as specified by SETMWL and GETMWL CCCs.

        mrl: c_uint16
            Maximum read length as specified by SETMRL and GETMRL CCCs.

        Returns
        -------
        dict:
            dictionary that indicates the result of the validation of the data

        """
        metadata = {
            "id": id,
            "memoryLayout": memoryLayout,
            "pid": pid,
            "bcr": bcr,
            "dcr": dcr,
            "staticAddress": staticAddress,
            "mwl": mwl,
            "mrl": mrl
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cTargetInitValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cTargetSetParameters(self, id: c_uint16, memoryLayout: I3cTargetMemoryLayout_t, pid: list, bcr: c_uint8, dcr: c_uint8, staticAddress: c_uint8, mwl: c_uint16 = 1024, mrl: c_uint16 = 1024) -> dict:
        """
        This function allows to change the parameters of the Supernova as an I3C target.

        Parameters
        ----------
        id : c_uint16
             An integer number that identifies the transfer.

        memoryLayout: I3cTargetMemoryLayout_t
            Layout of the memory that the target represents.

        pid: list
            List of 6 bytes that represents the 48-bit Provisioned ID (PID).

        bcr: c_uint8
            Bus Characteristics Register.

        dcr: I3cTargetDcr_t
            Device Characteristics Register. Determines the type of device the Supernova represents.
            The enum I3cTargetDcr_t provides 3 predefined DCR values.

        staticAddress: c_uint8
            I2C static address of the Supernova.

        mwl: c_uint16
            Maximum write length as specified by SETMWL and GETMWL CCCs.

        mrl: c_uint16
            Maximum read length as specified by SETMRL and GETMRL CCCs.

        Returns
        -------
        dict:
            dictionary that indicates the result of the validation of the data

        """
        metadata = {
            "id": id,
            "memoryLayout": memoryLayout,
            "pid": pid,
            "bcr": bcr,
            "dcr": dcr,
            "staticAddress": staticAddress,
            "mwl": mwl,
            "mrl": mrl
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cTargetSetParametersValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cTargetWriteMemory(self, id: c_uint16, memoryAddress: c_uint16, data: list) -> dict:
        """
        This function is in charge of modifying the data set by the user for the I3C_TARGET_WRITE_MEMORY command to be later sent to the Supernova (in I3C target mode)
        via USB. It calls i3cTargetWriteMemValidator which validates the data and serializes it using i3cTargetWriteMemSerializer.

        Parameters
        ----------
        id : c_uint16
             An integer number that identifies the transfer.

        memoryAddress: c_uint16
            Address of the memory to start to write

        data: list
            List of bytes that represents the data the user wants to write

        Returns
        -------
        dict:
            dictionary that indicates the result of the validation of the data        

        """

        metadata = {
            "id" : id,
            "memoryAddress": memoryAddress,
            "data" : data,
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cTargetWriteMemoryValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def i3cTargetReadMemory(self, id: c_uint16, memoryAddress: c_uint16, length: c_uint16) -> dict:
        """
        This function is in charge of modifying the data set by the user for the I3C_TARGET_READ_MEMORY command to be later sent to the Supernova (in I3C target mode)
        via USB. It calls i3cTargetReadMemValidator which validates the data and serializes it using i3cTargetReadMemSerializer.

        Parameters
        ----------
        id : c_uint16
             An integer number that identifies the transfer.

        memoryAddress: c_uint16
            Address of the memory to start reading from.

        length: c_uint16
            Data length the user intends to read

        Returns
        -------
        dict:
            dictionary that indicates the result of the validation of the data        

        """

        metadata = {
            "id" : id,
            "memoryAddress": memoryAddress,
            "length": length,
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = i3cTargetReadMemoryValidator(metadata)

        # If the command was built successfully, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()
    
    # CCC Wrappers ----------------------------------------------------------------------

    @__checkConnection
    def i3cGETBCR(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method gets the Bus Characteristics Register (BCR) from a target device on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the BCR.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETBCR
        DATA_LEN        = 1
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETDCR(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method gets the Device Characteristics Register (DCR) from a target device on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the DCR.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETDCR
        DATA_LEN        = 1
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETPID(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method gets the Provisioned ID (PID) from a target device on the I3C bus in MSB order.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the PID.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        -------
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETPID
        DATA_LEN        = 6
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETACCCR(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method gets the Accept Controller Role (ACCCR) from a target device on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the ACCCR.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETACCCR
        DATA_LEN        = 1
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETMXDS(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method gets the Maximum Data Speed (MXDS) from a target device on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the MXDS.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETMXDS
        DATA_LEN        = 5
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETMRL(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method gets the Maximum Read Length (MRL) from a target device on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the MRL.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETMRL
        DATA_LEN        = 3                                     # Maximum possible number of bytes returned. See Section 5.1.9.3.6 Set/Get Max Read Length (SETMRL/GETMRL) in MIPI I3C Basic V1.1.1 specifications.
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETMWL(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method gets the Maximum Write Length (MWL) from a target device on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the MWL.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETMWL
        DATA_LEN        = 2
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETXTIME(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method gets the Exchange Timing Support Information (XTIME) from a target device on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the XTIME.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETXTIME
        DATA_LEN        = 4
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETCAPS(self, id: c_uint16, targetAddress: c_uint8, defByte: c_uint8 = None) -> dict:
        """
        This method gets the Optional Feature Capabilities (CAPS) from a target device on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The address of the target device from which to get the CAPS.

        defByte : c_uint8
            The defining byte for the GETCAPS Format 2 version of the CCC. If not provided, the default value is None
            and it is assumed the Format 1 of the CCC.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_GETCAPS
        DATA_LEN        = 4
        DATA            = []
        DEF_BYTE        = 0x00

        if defByte is not None:
            CMD_TYPE = I3cCccType.CCC_WITH_DEFINING_BYTE
            DEF_BYTE = defByte

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, DEF_BYTE, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cRSTDAA(self, id: c_uint16) -> dict:
        """
        This method resets all Dynamic Address Assignment (DAA) activity on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_RSTDAA
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastENEC(self, id: c_uint16, events: list) -> dict:
        """
        This method broadcasts the Enable Target Events Command (ENEC) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID.The range allowed is [1, 65535].

        events : list
            A list containing events to be enabled.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        CMD_TYPE        = I3cCccType.CCC_WITH_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_ENEC
        DATA_LEN        = 0x01
        DATA            = []

        # Get target events byte
        eventsByte       = 0
        for event in events:
            eventsByte |= event.value

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, eventsByte, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastDISEC(self, id: c_uint16, events: list) -> dict:
        """
        This method broadcasts the Disable Target Events Command (DISEC) on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        events : list
            A list containing events to be disabled.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITH_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_DISEC
        DATA_LEN        = 0x01
        DATA            = []

        # Get target events byte
        eventsByte       = 0
        for event in events:
            eventsByte |= event.value

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, eventsByte, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectENEC(self, id: c_uint16, targetAddress: c_uint8, events: list) -> dict:
        """
        This method directly Enables Target Events Command (ENEC) to a specific target address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The specific target address to which ENEC is sent.

        events : list
            A list containing events to be enabled.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_ENEC
        DATA_LEN        = 0x01

        # Get target events byte
        eventsByte       = 0
        for event in events:
            eventsByte |= event.value

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CODE, DATA_LEN, [eventsByte])

    @__checkConnection
    def i3cDirectDISEC(self, id: c_uint16, targetAddress: c_uint8, events: list) -> dict:
        """
        This method directly Disables Target Events Command (DISEC) to a specific target address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The specific target address to which DISEC is sent.

        events : list
            A list containing events to be disabled.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_DISEC
        DATA_LEN        = 0x01

        # Get target events byte
        eventsByte       = 0
        for event in events:
            eventsByte |= event.value

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CODE, DATA_LEN, [eventsByte])

    @__checkConnection
    def i3cSETNEWDA(self, id: c_uint16, oldAddress: c_uint8, newAddress: c_uint8) -> dict:
        """
        This method Sets a New Dynamic Address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        oldAddress : c_uint8
            The old dynamic address to be replaced.

        newAddress : c_uint8
            The new dynamic address to be set.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        # TODO: Test. Add change in target device Table.
        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_SETNEWDA
        DATA_LEN        = 0x01
        DATA            = [(newAddress << 1)]
        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, oldAddress, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cSETDASA(self, id: c_uint16, staticAddress: c_uint8, dynamicAddress: c_uint8) -> dict:
        """
        This method Sets Dynamic Address from Static Address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [0, 65535].

        staticAddress : c_uint8
            The static address to be set.

        dynamicAddress : c_uint8
            The dynamic address to be set.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_SETDASA
        DATA_LEN        = 0x01
        DATA            = [(dynamicAddress << 1)]
        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, staticAddress, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cSETAASA(self, id: c_uint16, staticAddresses: list) -> dict:
        """
        This method sets the Dynamic Addresses from the Static Addresses on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [0, 65535].

        staticAddresses : list
            The static addresses of the targets.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_SETAASA
        DATA_LEN        = len(staticAddresses)
        DATA            = staticAddresses

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, I3C_BROADCAST_ADDRESS, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cENTDAA(self, id: c_uint16, targetDeviceTable: dict = None) -> dict:
        """
        This method is used to assign the dynamic address of the targets in the I3C bus using ENTDAA.

        Parameters
        ----------
        id : int
            A 2-byte integer representing the initialization ID. The range allowed is [1, 65535].

        targetDeviceTable : dict, optional
            A dictionary containing information about the target devices connected to the I3C bus.
            The default value is None.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        # Convert targetDeviceTable into a list of bytes

        entryList = []

        if targetDeviceTable is not None:
            for target in targetDeviceTable.values():

                configuration = target["configuration"]["targetType"].value |\
                                target["configuration"]["IBIRequest"].value |\
                                target["configuration"]["CRRequest"].value |\
                                target["configuration"]["daaUseSETDASA"].value |\
                                target["configuration"]["daaUseSETAASA"].value |\
                                target["configuration"]["daaUseENTDAA"].value |\
                                target["configuration"]["ibiTimestampEnable"].value |\
                                target["configuration"]["pendingReadCapability"].value

                entryList.append(target['staticAddress'])
                entryList.append(target['dynamicAddress'])
                entryList.extend(target['pid'])
                entryList.append(target['bcr'])
                entryList.append(target['dcr'])
                entryList.append(0) #mwl
                entryList.append(0) #mrl
                entryList.append(0) #maxIbiPayloadLength
                entryList.append(configuration)

        # Create the request

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_ENTDAA
        DATA_LEN        = len(entryList)
        DATA            = entryList

        # API I3C Send CCC. ENTDAA has an specific push pull and open drain frequency set in firmware, the ones sent below are not really used.
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, I3C_BROADCAST_ADDRESS, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectSETGRPA(self, id: c_uint16, targetAddress: c_uint8, grpa: c_uint8) -> dict:
        """
        This method sets Group Address on a specific target address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The specific target address on which to set GRPA.

        grpa : c_uint8
            The value to be set in the Group Address.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_SETGRPA
        DATA_LEN        = 1                                     # Group Address to set. See Section 5.1.9.3.27
        DATA            = [(grpa << 1)]                         # We need to shift the group address by 1 bit to the left.

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastRSTGRPA(self, id: c_uint16) -> dict:
        """
        This method broadcasts a Reset Group Address command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_RSTGRPA
        DATA_LEN        = 0                                     # Group Address to set. See Section 5.1.9.3.28
        DATA            = []
        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectRSTGRPA(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method sends a Resets Group Address command to a specific target address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The specific target address to which RSTGRPA is sent.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_RSTGRPA
        DATA_LEN        = 0
        DATA            = []                                    # Group Address to set. See Section 5.1.9.3.27

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectSETMRL(self, id: c_uint16, targetAddress: c_uint8, mrl: c_uint16, ibiPayloadSize: c_uint8 = None) -> dict:
        """
        This method directly sets the Maximum Read Length (MRL) for a specific target address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The specific target address for which MRL is set.

        mrl : c_uint16
            The value to be set as the Maximum Read Length.

        ibiPayloadSize : c_uint8
            Optional value to be set as the Maximum IBI Payload Size.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_SETMRL
        DATA            = [(mrl >> 8), (mrl)]
        if (ibiPayloadSize != None):
            DATA = DATA + [ibiPayloadSize]
        DATA_LEN        = len(DATA)

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectSETMWL(self, id: c_uint16, targetAddress: c_uint8, mwl: c_uint16) -> dict:
        """
        This method directly sets the Maximum Write Length (MWL) for a specific target address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The specific target address for which MWL is set.

        mwl : c_uint16
            The value to be set as the Maximum Write Length.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_SETMWL
        DATA_LEN        = 2
        DATA            = [(mwl >> 8), (mwl)]

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, 0x00, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastSETMWL(self, id: c_uint16, mwl: c_uint16) -> dict:
        """
        This method broadcasts the setting of Maximum Write Length (MWL) to all devices on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        mwl : c_uint16
            The value to be set as the Maximum Write Length for all devices.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_SETMWL
        DATA_LEN        = 2
        DATA            = [(mwl >> 8), (mwl)]
        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastSETMRL(self, id: c_uint16, mrl: c_uint16, ibiPayloadSize: c_uint8 = None) -> dict:
        """
        This method broadcasts the setting of Maximum Read Length (MRL) to all devices on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        mrl : c_uint16
            The value to be set as the Maximum Read Length for all devices.

        ibiPayloadSize : c_uint8
            Optional value to be set as the Maximum IBI Payload Size.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_SETMRL
        DATA            = [(mrl >> 8), (mrl)]
        if (ibiPayloadSize != None):
            DATA = DATA + [ibiPayloadSize]
        DATA_LEN        = len(DATA)

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastENDXFER(self, id: c_uint16, definingByte:c_uint8, data:list = []) -> dict:
        """
        This method broadcasts the Data Transfer Ending Procedure Control (ENDXFER) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        definingByte : c_uint8
            The defining byte for the ENDXFER command.

        data : list, optional
            Additional data for the ENDXFER command, default is an empty list.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITH_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_ENDXFER

        DATA_LEN        = 0x00
        aux_data = []
        if (data):
            aux_data.extend(data)
        DATA            = aux_data
        DATA_LEN        = len(DATA)

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, definingByte, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectENDXFER(self, id: c_uint16, targetAddress, definingByte: c_uint8, data:c_uint8 = 0, direction: TransferDirection = TransferDirection.WRITE) -> dict:
        """
        This method directly sends the Data Transfer Ending Procedure Control (ENDXFER) command to a specific target address on the I3C bus..

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The specific target address to which ENDXFER is sent.

        definingByte : c_uint8
            The defining byte for the ENDXFER command. It is always required.

        data : c_uint8
            Additional data for the ENDXFER command. This byte is only required for WRITE transfers.

        direction : TransferDirection
            It is an enum that indicates the direction of the transfer. The allowed values are READ or WRITE. The default value is WRITE.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITH_DEFINING_BYTE
        TARGET_ADDR     = targetAddress
        DIRECTION       = direction
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_ENDXFER
        DATA_LEN        = 0x01      # Up to I3C v1.2, only one byte is written or read. 
        DATA            = [data]    # If the direction is READ, then the default value will be sent but ignored by the firwmare.

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, definingByte, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastSETXTIME(self, id: c_uint16, subCMDByte:c_uint8, data:list = []) -> dict:
        """
        This method broadcasts the Set Exchange Timing Information (SETXTIME) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        subCMDByte : c_uint8
            The sub-command byte for the SETXTIME command.

        data : list, optional
            Additional data for the SETXTIME command, default is an empty list.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_SETXTIME
        DATA_LEN        = 0x01
        aux_data = [subCMDByte]
        if (data):
            aux_data.extend(data)
        DATA            = aux_data
        DATA_LEN        = len(DATA)

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectSETXTIME(self, id: c_uint16, targetAddress, subCMDByte:c_uint8, data:list = []) -> dict:
        """
        This method directly sends the Set Exchange Timing Information (SETXTIME) command to a specific target address on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        targetAddress : c_uint8
            The specific target address to which SETXTIME is sent.

        subCMDByte : c_uint8
            The sub-command byte for the SETXTIME command.

        data : list, optional
            Additional data for the SETXTIME command, default is an empty list.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = targetAddress
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_SETXTIME

        aux_data = [subCMDByte]
        if (data):
            aux_data.extend(data)
        DATA            = aux_data
        DATA_LEN        = len(DATA)

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastSETBUSCON(self, id: c_uint16, context:c_uint8, data:list = []) -> dict:
        """
        This method broadcasts the Set Bus Context (SETBUSCON) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        context : c_uint8
            The context value for the SETBUSCON command.

        data : list, optional
            Additional data for the SETBUSCON command, default is an empty list.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITH_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_SETBUSCON
        DATA_LEN        = 0x01

        aux_data = [context]
        if (data):
            aux_data.extend(data)
        DATA            = aux_data
        DATA_LEN        = len(DATA)

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastENTAS0(self, id: c_uint16) -> dict:
        """
        This method broadcasts the Enter Activity State 0 (ENTAS0) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_ENTAS0
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectENTAS0(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method emits the Enter Activity State 0 (ENTAS0) command on the I3C bus to a specific target address.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].
        
        targetAddress : c_uint8
            The specific target address to which the Direct ENTAS0 CCC is sent.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = targetAddress
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_ENTAS0
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)


    @__checkConnection
    def i3cBroadcastENTAS1(self, id: c_uint16) -> dict:
        """
        This method broadcasts the Enter Activity State 1 (ENTAS1) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_ENTAS1
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)
    
    @__checkConnection
    def i3cDirectENTAS1(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method emits the Enter Activity State 1 (ENTAS1) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].
        
        targetAddress : c_uint8
            The specific target address to which the Direct ENTAS1 CCC is sent.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = targetAddress
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_ENTAS1
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastENTAS2(self, id: c_uint16) -> dict:
        """
        This method broadcasts the Enter Activity State 2 (ENTAS2) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """
        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_ENTAS2
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectENTAS2(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method emits the Enter Activity State 2 (ENTAS2) command on the I3C bus to a specific target address.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].
        
        targetAddress : c_uint8
            The specific target address to which the Direct ENTAS2 CCC is sent.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = targetAddress
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_ENTAS2
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastENTAS3(self, id: c_uint16) -> dict:
        """
        This method broadcasts the Enter Activity State 3 (ENTAS3) command on the I3C bus.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.B_ENTAS3
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectENTAS3(self, id: c_uint16, targetAddress: c_uint8) -> dict:
        """
        This method emits the Enter Activity State 3 (ENTAS3) command on the I3C bus to a specific target address.

        Parameters
        ----------
        id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].
        
        targetAddress : c_uint8
            The specific target address to which the Direct ENTAS3 CCC is sent.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.
        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = targetAddress
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_ENTAS3
        DATA_LEN        = 0x00
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, 0x00, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cGETSTATUS(self, id: c_uint16, targetAddress: c_uint8, defByte: c_uint8 = None) -> dict:
        """
        This method is used to request to the Supernova controller to perform a GET_STATUS CCC.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        targetAddress : int
            It is a 1-byte integer that indicates the dynamic address of the target this command is directed to.

        defByte : c_uint8
            The defining byte for the GETSTATUS Format 2 version of the CCC. If not provided, the default value is None
            and it is assumed the Format 1 of the CCC.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        CMD_TYPE        = I3cCccType.CCC_WITHOUT_DEFINING_BYTE
        TARGET_ADDR     = targetAddress
        DIRECTION       = TransferDirection.READ
        MODE            = TransferMode.I3C_SDR
        CCC_CODE        = CCC.D_GETSTATUS
        DATA_LEN        = 2
        DATA            = []
        DEF_BYTE        = 0x00

        if defByte is not None:
            CMD_TYPE = I3cCccType.CCC_WITH_DEFINING_BYTE
            DEF_BYTE = defByte

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, DEF_BYTE, CCC_CODE, DATA_LEN, DATA)

    @__checkConnection
    def i3cBroadcastRSTACT(self, id: c_uint16, defByte: c_uint8) -> dict:
        """
        This method is used to broadcast the Reset Action (RSTACT) command to all devices on the I3C bus.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        defByte : int
            It is a 1-byte integer that indicates the defining byte for the RSTACT command.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        CMD_TYPE        = I3cCccType.CCC_WITH_DEFINING_BYTE
        TARGET_ADDR     = 0x7E
        DIRECTION       = TransferDirection.WRITE
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.B_RSTACT
        DATA_LEN        = 1
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, TARGET_ADDR, MODE, defByte.value, CCC_CMD, DATA_LEN, DATA)

    @__checkConnection
    def i3cDirectRSTACT(self, id: c_uint16, targetAddress: c_uint8, defByte: c_uint8, direction: TransferDirection) -> dict:
        """
        This method is used to send the Reset Action (RSTACT) command to a specific target address on the I3C bus.
        
        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The allowed range is [1, 65535].

        targetAddress : int
            It is a 1-byte integer that indicates the dynamic address of the target this command is directed to.

        defByte : int
            It is a 1-byte integer that indicates the defining byte for the RSTACT command.

        direction : TransferDirection
            It is an enum that indicates the direction of the transfer. The allowed values are READ or WRITE.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        CMD_TYPE        = I3cCccType.CCC_WITH_DEFINING_BYTE
        DIRECTION       = direction
        MODE            = TransferMode.I3C_SDR
        CCC_CMD         = CCC.D_RSTACT
        DATA_LEN        = 0
        if (direction == TransferDirection.READ):
            DATA_LEN        = 1
        DATA            = []

        # API I3C Send CCC
        return self.i3cControllerCccTransfer(id, CMD_TYPE, DIRECTION, targetAddress, MODE, defByte.value, CCC_CMD, DATA_LEN, DATA)

    # --------------------------UART management --------------------------------------------------------------------

    # ------------------------------UART INIT ----------------------------#
    @__checkConnection
    def uartInit(self, id: int, baudrate: UartBaudRate, hardwareHandshake:bool, parityMode:UartParity, dataSize:UartDataSize, stopBit: UartStopBit ) -> dict:
        """
        This method initializes the UART peripherals

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        baudrate : UartBaudRate
            This parameter represents the UART TX and RX frequency from the options provided by the UartBaudRate enum.
            The frequency goes from 600bps to up to 115200bps.

        hardwareHandshake : bool
            This parameter represents a boolean flag to enable or disable this option.

        parityMode: UartParity
            This parameter represents the different parity modes available in the UartParity enum.
            The parity modes are: none, even or odd.

        dataSize: UartDataSize
            This parameter represents the different data sizes available in the UartDataSize enum.
            The data sizes are either 7 or 8.

        stopBit: UartStopBit
            This parameter represent the different stop bit configuration available in the UartStopBit enum.
            The stop bit can be of size 1 or 2.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "baudRate": baudrate,
            "hardwareHandshake": hardwareHandshake,
            "parityMode": parityMode,
            "dataSize": dataSize,
            "stopBitType" : stopBit,
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = uartInitValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    # ------------------------------UART SET ----------------------------#
    @__checkConnection
    def uartSetParameters(self, id: int, baudrate: UartBaudRate, hardwareHandshake:bool, parityMode:UartParity, dataSize:UartDataSize, stopBit: UartStopBit ) -> dict:
        """
        This method sets the UART peripheral parameters

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The range allowed is [1, 65535].

        baudrate : UartBaudRate
            This parameter represents the UART TX and RX frequency from the options provided by the UartBaudRate enum.
            The frequency goes from 600bps to up to 115200bps.

        hardwareHandshake : bool
            This parameter represents a boolean flag to enable or disable this option.

        parityMode: UartParity
            This parameter represents the different parity modes available in the UartParity enum.
            The parity modes are: none, even or odd.

        dataSize: UartDataSize
            This parameter represents the different data sizes available in the UartDataSize enum.
            The data sizes are either 7 or 8.

        stopBit: UartStopBit
            This parameter represent the different stop bit configuration available in the UartStopBit enum.
            The stop bit can be of size 1 or 2.


        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "baudRate": baudrate,
            "hardwareHandshake": hardwareHandshake,
            "parityMode": parityMode,
            "dataSize": dataSize,
            "stopBitType" : stopBit,
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = uartSetParametersValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()
    
    # ------------------------------UART SEND ----------------------------#
    @__checkConnection
    def uartSendMessage(self, id: int, data: list) -> dict:
        """
        This method is used to request to the the Supernova device to perform an UART send transfer.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represent the transfer id. The range allowed is [1, 65535].

        data : list
            Python list that contains the data transferred in the UART Send. The list holds
            bytes elements, and the maximum length is 1024 bytes.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "data" : data
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = uartSendValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()
    
    # SPI management --------------------------------------------------------------------

    @__checkConnection
    def spiControllerInit(self,
                          id: int,
                          bitOrder: SpiControllerBitOrder,
                          mode: SpiControllerMode,
                          dataWidth: SpiControllerDataWidth,
                          chipSelect: SpiControllerChipSelect,
                          chipSelectPol: SpiControllerChipSelectPolarity,
                          frequency: c_uint32) -> dict:
        """
        This method initializes the SPI peripheral with the specified configuration.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        bitOrder : SpiControllerBitOrder
            Sets the bit order of the SPI peripheral, could be SpiControllerBitOrder.MSB or SpiControllerBitOrder.LSB.
        
        mode : SpiControllerMode
            Sets the SPI mode, could be SpiControllerMode.MODE_0, SpiControllerMode.MODE_1, SpiControllerMode.MODE_2 or SpiControllerMode.MODE_3.
        
        dataWidth : SpiControllerDataWidth
            Sets the SPI data width, could be SpiControllerDataWidth._8_BITS_DATA, SpiControllerDataWidth._16_BITS_DATA.

        chipSelect : SpiControllerChipSelect
            Sets the SPI chip select, could be SpiControllerChipSelect.CHIP_SELECT_0, SpiControllerChipSelect.CHIP_SELECT_1,
            SpiControllerChipSelect.CHIP_SELECT_2 or SpiControllerChipSelect.CHIP_SELECT_3.

        chipSelectPol : SpiControllerChipSelectPolarity
            Sets the SPI chip select polarity, could be SpiControllerChipSelectPolarity.ACTIVE_LOW or SpiControllerChipSelectPolarity.ACTIVE_HIGH.
        
        frequency : c_uint32
            Sets the SPI Clock frequency in Hz. Currently, the minimum allowed value is 10000 Hz and the maximum allowed value is 50000000 Hz.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "bitOrder" : bitOrder,
            "mode" : mode,
            "dataWidth" : dataWidth,
            "chipSelect" : chipSelect,
            "chipSelectPol" : chipSelectPol,
            "frequency" : frequency
        }
        
        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = spiControllerInitValidator(metadata)
        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def spiControllerSetParameters(self,
                                   id: int,
                                   bitOrder: SpiControllerBitOrder,
                                   mode: SpiControllerMode,
                                   dataWidth: SpiControllerDataWidth,
                                   chipSelect: SpiControllerChipSelect,
                                   chipSelectPol: SpiControllerChipSelectPolarity,
                                   frequency: c_uint32) -> dict:
        """
        This method sets the SPI peripheral configuration.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        bitOrder : SpiControllerBitOrder
            Sets the bit order of the SPI peripheral, could be SpiControllerBitOrder.MSB or SpiControllerBitOrder.LSB.
        
        mode : SpiControllerMode
            Sets the SPI mode, could be SpiControllerMode.MODE_0, SpiControllerMode.MODE_1, SpiControllerMode.MODE_2 or SpiControllerMode.MODE_3.
        
        dataWidth : SpiControllerDataWidth
            Sets the SPI data width, could be SpiControllerDataWidth._8_BITS_DATA, SpiControllerDataWidth._16_BITS_DATA.

        chipSelect : SpiControllerChipSelect
            Sets the SPI chip select, could be SpiControllerChipSelect.CHIP_SELECT_0, SpiControllerChipSelect.CHIP_SELECT_1,
            SpiControllerChipSelect.CHIP_SELECT_2 or SpiControllerChipSelect.CHIP_SELECT_3.

        chipSelectPol : SpiControllerChipSelectPolarity
            Sets the SPI chip select polarity, could be SpiControllerChipSelectPolarity.ACTIVE_LOW or SpiControllerChipSelectPolarity.ACTIVE_HIGH.
        
        frequency : c_uint32
            Sets the SPI Clock frequency in Hz. Currently, the minimum allowed value is 10000 Hz and the maximum allowed value is 50000000 Hz.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "bitOrder" : bitOrder,
            "mode" : mode,
            "dataWidth" : dataWidth,
            "chipSelect" : chipSelect,
            "chipSelectPol" : chipSelectPol,
            "frequency" : frequency
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = spiControllerSetParametersValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def spiControllerTransfer(self, id: int, transferLength: int, payload: list) -> dict:
        """
        This method performs a SPI transfer.
        
        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        transferLength : int
            It is a 2-bytes integer that represents the transfer length. The range allowed is [1, 1024].

        payload : list  
            Python list that contains the SPI data transferred. The list holds bytes elements and
            the maximum length is 1024 bytes.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "transferLength" : transferLength,
            "payload" : payload
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = spiControllerTransferValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def gpioConfigurePin(self, id: int, pinNumber: GpioPinNumber, functionality: GpioFunctionality, initialOutputLogicLevel: GpioLogicLevel = GpioLogicLevel.LOW) -> dict:
        """
        This method configures a GPIO pin with the specified functionality.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        pinNumber : GpioPinNumber
            An enum representing the GPIO pin number to configure.

        functionality : GpioFunctionality
            An enum representing the desired functionality for the GPIO pin.
        
        initialOutputLogicLevel : GpioLogicLevel
            An enum representing the initial output logic level for the GPIO pin. This parameter is optional
            and only required when the GPIO pin is configured as an output.
            This feature is reserved for future use.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "pinNumber" : pinNumber,
            "functionality" : functionality,
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = gpioConfigurePinValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def gpioDigitalWrite(self, id: int, pinNumber: GpioPinNumber, logicLevel: GpioLogicLevel) -> dict:
        """
        This method writes a digital logic level to a GPIO pin.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        pinNumber : GpioPinNumber
            An enum representing the GPIO pin number to write to.

        logicLevel : GpioLogicLevel
            An enum representing the logic level to write to the GPIO pin.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """

        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "pinNumber" : pinNumber,
            "logicLevel" : logicLevel,
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = gpioDigitalWriteValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def gpioDigitalRead(self, id: int, pinNumber: GpioPinNumber) -> dict:
        """
        This method reads the digital logic level from a GPIO pin.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        pinNumber : GpioPinNumber
            An enum representing the GPIO pin number to read from.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
 
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "pinNumber" : pinNumber
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = gpioDigitalReadValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def gpioSetInterrupt(self, id: int, pinNumber: GpioPinNumber, trigger: GpioTriggerType) -> dict:
        """
        This method sets an interruption to a GPIO pin.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        pinNumber : GpioPinNumber
            An enum representing the GPIO pin number to read from.

        trigger : GpioTriggerType
        The trigger type used for the interruption. Must be one of the options provided by the GpioTriggerType enum.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
 
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "pinNumber" : pinNumber,
            "trigger": trigger
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = gpioSetInterruptValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()

    @__checkConnection
    def gpioDisableInterrupt(self, id: int, pinNumber: GpioPinNumber) -> dict:
        """
        This method disables interruptions of a GPIO pin.

        Parameters
        ----------
        id : int
            It is a 2-bytes integer that represents the transfer id. The range allowed is [1, 65535].

        pinNumber : GpioPinNumber
            An enum representing the GPIO pin number to read from.

        Returns
        -------
        dict
            Return the SystemMessage in dictionary format.

        """
 
        # Create Python dict that contains the command required data.
        metadata = {
            "id" : id,
            "pinNumber" : pinNumber
        }

        # Check data validation and serialize the USB request.
        requestSerialization, responseInstance, result = gpioDisableInterruptValidator(metadata)

        # If the command was built successfuly, send it to the device
        if result.opcode == RequestValidatorOpcode.SUCCESS:

            # Generate a pair request-response
            request_metadata = {
                "id": id,
                "request": requestSerialization,
                "response": responseInstance
            }

            self.__sendMessage(request_metadata, result)

        # Return result in dict format.
        return result.toDictionary()