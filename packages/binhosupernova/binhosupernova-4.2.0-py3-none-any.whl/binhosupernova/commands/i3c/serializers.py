from .definitions import *

#================================================================================#
# region I3C CONTROLLER INIT SERIALIZER
#================================================================================#

def i3cControllerInitSerializer(id: c_uint16, pushPullFrequency: I3cPushPullTransferRate, i3cOpenDrainFrequency: I3cOpenDrainTransferRate, i2cOpenDrainFrequency: I2cTransferRate, driveStrength: I3cDriveStrength) -> tuple[bytes,I3cControllerInitResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER INIT request and return the corresponding response instance.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    pushPullFrequency: I3cPushPullTransferRate
        I3C Push-Pull frequency
    i3cOpenDrainFrequency: I3cOpenDrainTransferRate
        I3C Open Drain frequency
    i2cOpenDrainFrequency: I2cTransferRate
        I2C Open Drain frequency
    driveStrength: I3cDriveStrength
        Drive strength of the I3C controller.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerInitRequest_t()

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_INIT.value

    command.fields.parameters.pushPullFrequency = pushPullFrequency.value
    command.fields.parameters.i3cOpenDrainFrequency = i3cOpenDrainFrequency.value
    command.fields.parameters.i2cOpenDrainFrequency = i2cOpenDrainFrequency.value
    command.fields.parameters.driveStrength = driveStrength.value

    return command.toBytes(), I3cControllerInitResponse_t()

#endregion

#================================================================================#
# region I3C CONTROLLER SET PARAMETERS SERIALIZER
#================================================================================#

def i3cControllerSetParametersSerializer(id: c_uint16, pushPullFrequency: I3cPushPullTransferRate, i3cOpenDrainFrequency: I3cOpenDrainTransferRate, i2cOpenDrainFrequency: I2cTransferRate, driveStrength: I3cDriveStrength) -> tuple[bytes,I3cControllerSetParametersResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER SET PARAMETERS request and return the corresponding response instance.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    pushPullFrequency: I3cPushPullTransferRate
        I3C Push-Pull frequency
    i3cOpenDrainFrequency: I3cOpenDrainTransferRate
        I3C Open Drain frequency
    i2cOpenDrainFrequency: I2cTransferRate
        I2C Open Drain frequency
    driveStrength: I3cDriveStrength
        Drive strength of the I3C controller.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerSetParametersRequest_t()

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_SET_PARAMETERS.value

    command.fields.parameters.pushPullFrequency = pushPullFrequency.value
    command.fields.parameters.i3cOpenDrainFrequency = i3cOpenDrainFrequency.value
    command.fields.parameters.i2cOpenDrainFrequency = i2cOpenDrainFrequency.value
    command.fields.parameters.driveStrength = driveStrength.value

    return command.toBytes(), I3cControllerSetParametersResponse_t()

#endregion

#================================================================================#
# region I3C CONTROLLER INIT BUS SERIALIZER
#================================================================================#

def i3cControllerInitBusSerializer(id: c_uint16, targetDevicesTable: dict = None) -> tuple[bytes,I3cControllerInitBusResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER INIT BUS request and return the corresponding response instance.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    targetDevicesTable : dict
        Python dict that contains the Target Device Table information.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerInitBusRequest_t()

    # Set endpoint ID and command opcode.
    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_INIT_BUS.value
    command.fields.parameters.numberOfTargets = 0

    if targetDevicesTable is not None:

        command.fields.parameters.numberOfTargets = len(targetDevicesTable)

        for i in range(command.fields.parameters.numberOfTargets):

            target = targetDevicesTable[i]

            tableEntry = I3cTargetDeviceEntry_t()

            # Addresses
            tableEntry.staticAddress = target["staticAddress"]
            tableEntry.dynamicAddress = target["dynamicAddress"]

            # Provisioned ID
            pid = target["pid"]
            tableEntry.pid.data[0:sizeof(I3cPidBytes_t)] = pid[0:sizeof(I3cPidBytes_t)]

            # BCR
            tableEntry.bcr.byte = target["bcr"]

            # DCR
            tableEntry.dcr = target["dcr"]

            # Lengths
            tableEntry.mwl = 0
            tableEntry.mrl = 0
            tableEntry.maxIbiPayloadLength = 0

            # Configuration
            configuration = I3cTargetConfiguration_t()
            configuration.fields.targetType = target["configuration"]["targetType"].value
            configuration.fields.acceptIbiRequest = target["configuration"]["IBIRequest"].value
            configuration.fields.acceptControllerRoleRequest = target["configuration"]["CRRequest"].value
            configuration.fields.daaUseSETDASA = target["configuration"]["daaUseSETDASA"].value
            configuration.fields.daaUseSETAASA = target["configuration"]["daaUseSETAASA"].value
            configuration.fields.daaUseENTDAA = target["configuration"]["daaUseENTDAA"].value
            configuration.fields.ibiTimestampEnable = target["configuration"]["ibiTimestampEnable"].value
            configuration.fields.pendingReadCapability = target["configuration"]["pendingReadCapability"].value
            tableEntry.configuration = configuration

            # Push table entry to command
            command.fields.payload[i] = tableEntry

    return command.toBytes(), I3cControllerInitBusResponse_t()

#endregion

#================================================================================#
# region I3C CONTROLLER RESET BUS SERIALIZER
#================================================================================#

def i3cControllerResetBusSerializer(id: c_uint16) -> tuple[bytes,I3cControllerResetBusResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER RESET BUS request and return the corresponding response instance.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerResetBusRequest_t()

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_RESET_BUS.value

    return command.toBytes(), I3cControllerResetBusResponse_t()

#endregion

#================================================================================#
# region I3C CONTROLLER GET TARGET DEVICES TABLE SERIALIZER
#================================================================================#

def i3cControllerGetTargetDevicesTableSerializer(id: c_uint16) -> tuple[bytes, I3cControllerGetTargetDevicesTableResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER GET TARGET DEVICES TABLE request and return the corresponding response instance.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command
    command = I3cControllerGetTargetDevicesTableRequest_t()

    # Set endpoint ID and command opcode
    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_GET_TARGET_DEVICES_TABLE.value

    return command.toBytes(), I3cControllerGetTargetDevicesTableResponse_t()

#endregion

#================================================================================#
# region I3C CONTROLLER SET TARGET DEVICE CONFIGURATION SERIALIZER
#================================================================================#

def i3cControllerSetTargetDeviceConfigurationSerializer(id: c_uint16, targetAddress: c_uint8, configuration: dict) -> tuple[bytes, I3cControllerSetTargetDeviceConfigurationResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER SET TARGET DEVICE CONFIGURATION request and return the corresponding response instance.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    targetAddress: c_uint8
            Target address whose configuration will be set.
    entry : dict
        Python dict that contains the target dynamic address and the new configuration.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    # Create command
    command = I3cControllerSetTargetDeviceConfigurationRequest_t()

    # Set endpoint ID and command opcode

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_SET_TARGET_DEVICE_CONFIG.value

    # Address
    command.fields.parameters.targetAddress = targetAddress

    # Configuration
    targetConfiguration = I3cTargetConfiguration_t()
    targetConfiguration.fields.targetType = configuration["targetType"].value
    targetConfiguration.fields.acceptIbiRequest = configuration["IBIRequest"].value
    targetConfiguration.fields.acceptControllerRoleRequest = configuration["CRRequest"].value
    targetConfiguration.fields.daaUseSETDASA = configuration["daaUseSETDASA"].value
    targetConfiguration.fields.daaUseSETAASA = configuration["daaUseSETAASA"].value
    targetConfiguration.fields.daaUseENTDAA = configuration["daaUseENTDAA"].value
    targetConfiguration.fields.ibiTimestampEnable = configuration["ibiTimestampEnable"].value
    targetConfiguration.fields.pendingReadCapability = configuration["pendingReadCapability"].value
    command.fields.parameters.configuration = targetConfiguration

    return command.toBytes(), I3cControllerSetTargetDeviceConfigurationResponse_t()

#endregion

#================================================================================#
# region I3C CONTROLLER PRIVATE TRANSFER SERIALIZERS
#================================================================================#

def i3cControllerWriteSerializer(id: c_uint16, targetAddress: c_uint8, mode: TransferMode, registerAddress: list, payload: list, startWith7E: bool = True, nonStop: bool = False)  -> tuple[bytes,I3cControllerPrivateTransferResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER PRIVATE TRANSFER request and return the corresponding response instance to issue an I3C Private Write transfer
    in SDR mode.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    targetAddress : c_uint8
        Target address.
    mode : TransferMode
        Transfer mode: I3C SDR, I3C HDR DDR, I2C, etc.
    registerAddress : list
        List that contains the target internal register address where the data is written.
    payload : list
        List that contains the data to be written.
    startWith7E: bool
        Boolean flag to indicate if the transfer must start with the broadcast address 0x7E.
    nonStop: bool
        Boolean flag to indicate whether or not the STOP condition must be issued at the end of the transfer or not.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerPrivateTransferRequest_t()

    # Header
    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_PRIVATE_TRANSFER.value

    # Parameters
    command.fields.parameters.targetAddress = targetAddress
    command.fields.parameters.direction = TransferDirection.WRITE.value
    command.fields.parameters.mode = mode.value
    command.fields.parameters.nonStop = c_uint8(nonStop).value
    command.fields.parameters.startWith7E = c_uint8(startWith7E).value
    command.fields.parameters.registerAddressLength = len(registerAddress)
    command.fields.parameters.payloadLength = len(payload)

    for i in range(len(registerAddress)):
        command.fields.parameters.registerAddress[i] = registerAddress[i]

    # Payload
    for i in range(len(payload)):
        command.fields.payload[i] = payload[i]

    return command.toBytes(), I3cControllerPrivateTransferResponse_t()

def i3cControllerReadSerializer(id: c_uint16, targetAddress: c_uint8, mode: TransferMode, registerAddress: list, length: c_uint16, startWith7E: bool = True, nonStop: bool = False) -> tuple[bytes,I3cControllerPrivateTransferResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER PRIVATE TRANSFER request and return the corresponding response instance to issue an I3C Private Read transfer in SDR mode.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    targetAddress : c_uint8
        Target address.
    mode : TransferMode
        Transfer mode: I3C SDR, I3C HDR DDR, I2C, etc.
    registerAddress : list
        List that contains the target internal register address where the data is written.
    length : c_uint16
        Number of bytes to read.
    startWith7E: bool
        Boolean flag to indicate if the transfer must start with the broadcast address 0x7E.
    nonStop: bool
        Boolean flag to indicate whether or not the STOP condition must be issued at the end of the transfer or not.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerPrivateTransferRequest_t()

    # Header
    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_PRIVATE_TRANSFER.value

    # Parameters
    command.fields.parameters.targetAddress = targetAddress
    command.fields.parameters.direction = TransferDirection.READ.value
    command.fields.parameters.mode = mode.value
    command.fields.parameters.nonStop = c_uint8(nonStop).value
    command.fields.parameters.startWith7E = c_uint8(startWith7E).value
    command.fields.parameters.registerAddressLength = len(registerAddress)
    command.fields.parameters.payloadLength = length

    for i in range(len(registerAddress)):
        command.fields.parameters.registerAddress[i] = registerAddress[i]

    return command.toBytes(), I3cControllerPrivateTransferResponse_t()

def i3cControllerHdrDdrWriteSerializer(id: c_uint16, targetAddress: c_uint8, hdrDdrCommand: c_uint8, payload: list) -> tuple[bytes,I3cControllerPrivateTransferResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER PRIVATE TRANSFER request and return the corresponding response instance to issue an I3C Private Write transfer in HDR-DDR mode.

    Arguments
    ---------
    id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

    targetAddress : c_uint8
        The address of the target device for writing data.

    hdrDdrCommand : c_uint8
        The HDR-DDR command.

    data : list
        A list containing the data to be written to the device. The length of this list must be a multple of 2.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerPrivateTransferRequest_t()

    # Header
    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_PRIVATE_TRANSFER.value

    # Parameters
    command.fields.parameters.targetAddress = targetAddress
    command.fields.parameters.direction = TransferDirection.WRITE.value
    command.fields.parameters.mode = TransferMode.I3C_HDR_DDR.value
    command.fields.parameters.hdrDdrCommand = hdrDdrCommand
    command.fields.parameters.payloadLength = len(payload)

    # Payload
    for i in range(len(payload)):
        command.fields.payload[i] = payload[i]

    return command.toBytes(), I3cControllerPrivateTransferResponse_t()

def i3cControllerHdrDdrReadSerializer(id: c_uint16, targetAddress: c_uint8, hdrDdrCommand: c_uint8, length: c_uint16) -> tuple[bytes,I3cControllerPrivateTransferResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER PRIVATE TRANSFER request and return the corresponding response instance to issue an I3C Private Read transfer in HDR-DDR mode.

    Arguments
    ---------
    id : c_uint16
            A 2-byte unsigned integer representing the transfer ID. The range allowed is [1, 65535].

    targetAddress : c_uint8
        The address of the target device for writing data.

    hdrDdrCommand : c_uint8
        The HDR-DDR command.

    length : c_uint16
            The length of the data to be read. The length must be multiple of 2.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerPrivateTransferRequest_t()

    # Header
    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_PRIVATE_TRANSFER.value

    # Parameters
    command.fields.parameters.targetAddress = targetAddress
    command.fields.parameters.direction = TransferDirection.READ.value
    command.fields.parameters.mode = TransferMode.I3C_HDR_DDR.value
    command.fields.parameters.hdrDdrCommand = hdrDdrCommand
    command.fields.parameters.payloadLength = length

    return command.toBytes(), I3cControllerPrivateTransferResponse_t()

#endregion

#================================================================================#
# region I3C CONTROLLER CCC TRANSFER SERIALIZER
#================================================================================#

def i3cControllerCccTransferSerializer(id: c_uint16, targetAddress: c_uint8, direction: TransferDirection, mode: TransferMode, commandType: I3cCccType, defByte: c_uint8, ccc: c_uint8, length: c_uint16, data: list, nonStop: bool = False):
    """
    This functions create and serializes an I3C CONTROLLER CCC TRANSFER request and return the corresponding response instance.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    targetAddress : c_uint8
        Target address.
    direction: TransferDirection
        CCC Transfer direction: Write or Read.
    mode : TransferMode
        Transfer mode: I3C SDR, I3C HDR DDR, I2C, etc.
    commandType : I3cCccType
        CCC type: With or without defining byte.
    defByte : c_uint8
        Defining byte in case cmdType indicates the command includes one
    ccc : c_uint8
        Code to send
    length : c_uint16
        Length of the data to be written or retrieved
    data : list
        List that contains the data to be written.
    nonStop: bool
        Boolean flag to indicate whether or not the STOP condition must be issued at the end of the transfer or not.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerCccTransferRequest_t()

     # Header
    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_CCC_TRANSFER.value

    # Parameters
    command.fields.parameters.targetAddress = targetAddress
    command.fields.parameters.direction = direction.value
    command.fields.parameters.mode = mode.value
    command.fields.parameters.nonStop = c_uint8(nonStop).value
    command.fields.parameters.type = commandType.value
    command.fields.parameters.ccc = ccc.value
    command.fields.parameters.definingByte = defByte

    if direction == TransferDirection.READ:
        command.fields.parameters.payloadLength = length
    else:
        command.fields.parameters.payloadLength = len(data)

    for i in range(len(data)):
        command.fields.payload[i] = data[i]

    return command.toBytes(), I3cControllerCccTransferResponse_t()

#endregion

#================================================================================#
# region I3C CONTROLLER TRIGGER PATTERN SERIALIZER
#================================================================================#

def i3cControllerTriggerPatternSerializer(id: c_uint16, pattern: I3cPattern) -> tuple[bytes, I3cControllerTriggerPatternResponse_t]:
    """
    This functions create and serializes an I3C CONTROLLER RIGGER PATTERN request and return the corresponding response instance.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    pattern: I3cPattern
        Identifier of the pattern to be triggered by the Supernova.

    Returns
    -------
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cControllerTriggerPatternRequest_t()

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_CONTROLLER_TRIGGER_PATTERN.value
    command.fields.parameters.pattern = pattern.value

    return command.toBytes(), I3cControllerTriggerPatternResponse_t()

#endregion

#================================================================================#
# region I3C TARGET SERIALIZERS
#================================================================================#

def i3cTargetInitSerializer(id: c_uint16, memoryLayout: I3cTargetMemoryLayout_t, pid: list, bcr: c_uint8, dcr: c_uint8, staticAddress: c_uint8, mwl: c_uint16 = 1024, mrl: c_uint16 = 1024) -> tuple[bytes,I3cTargetInitResponse_t]:
    """
    This functions create and serializes an I3C TARGET INIT request and return the corresponding response instance.

    Arguments
    ---------
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
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cTargetInitRequest_t()

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_TARGET_INIT.value

    command.fields.parameters.memoryLayout = memoryLayout.value

    PID = I3cPID_t.from_buffer_copy(bytes(pid))

    partNo = (PID.bytes.PID_3 << 24 | PID.bytes.PID_2 << 16 | PID.bytes.PID_1 << 8 | PID.bytes.PID_0)
    randomValueFlag = (0x01 & PID.bytes.PID_4)
    vendorId = ((PID.bytes.PID_5 << 8 | PID.bytes.PID_4) >> 1)

    command.fields.parameters.partNo = partNo
    command.fields.parameters.randomValueFlag = randomValueFlag
    command.fields.parameters.vendorId = vendorId
    command.fields.parameters.bcr.byte = bcr
    command.fields.parameters.dcr = dcr.value
    command.fields.parameters.staticAddress = staticAddress
    command.fields.parameters.mwl = mwl
    command.fields.parameters.mrl = mrl

    return command.toBytes(), I3cTargetInitResponse_t()

def i3cTargetSetParametersSerializer(id: c_uint16, memoryLayout: I3cTargetMemoryLayout_t, pid: list, bcr: c_uint8, dcr: c_uint8, staticAddress: c_uint8, mwl: c_uint16 = 1024, mrl: c_uint16 = 1024) -> tuple[bytes,I3cTargetSetParametersResponse_t]:
    """
    This functions create and serializes an I3C TARGET SET PARAMETERS request and return the corresponding response instance.

    Arguments
    ---------
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
    tuple
        Command serialization to be sent to the device and the response instance.

    """
    command = I3cTargetSetParametersRequest_t()

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_TARGET_SET_PARAMETERS.value

    command.fields.parameters.memoryLayout = memoryLayout.value

    PID = I3cPID_t.from_buffer_copy(bytes(pid))

    partNo = (PID.bytes.PID_3 << 24 | PID.bytes.PID_2 << 16 | PID.bytes.PID_1 << 8 | PID.bytes.PID_0)
    randomValueFlag = (0x01 & PID.bytes.PID_4)
    vendorId = ((PID.bytes.PID_5 << 8 | PID.bytes.PID_4) >> 1)

    command.fields.parameters.partNo = partNo
    command.fields.parameters.randomValueFlag = randomValueFlag
    command.fields.parameters.vendorId = vendorId
    command.fields.parameters.bcr.byte = bcr
    command.fields.parameters.dcr = dcr.value
    command.fields.parameters.staticAddress = staticAddress
    command.fields.parameters.mwl = mwl
    command.fields.parameters.mrl = mrl

    return command.toBytes(), I3cTargetSetParametersResponse_t()

def i3cTargetWriteMemorySerializer(id: c_uint16, memoryAddress: c_uint16, data: list) -> tuple[bytes, I3cTargetTransferMemoryResponse_t]:
    """
    This function performs an I3C TARGET WRITE MEM command.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    memoryAddress : c_uint16
        Register address of the target memory to start writing.
    data : list
        List that contains the data to be written.

    Returns
    -------
    tuple
        Command list with the commands to be sent to the USB device and the response instance.

    """
    command = I3cTargetTransferMemoryRequest_t()

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_TARGET_WRITE_MEMORY.value

    command.fields.parameters.memoryAddress = memoryAddress
    command.fields.parameters.payloadLength = len(data)

    # Data Block
    for i in range(len(data)):
        command.fields.payload[i] = data[i]

    return command.toBytes(), I3cTargetTransferMemoryResponse_t()

def i3cTargetReadMemorySerializer(id: c_uint16, memoryAddress: c_uint16, length: c_uint16) -> tuple[bytes, I3cTargetTransferMemoryResponse_t]:
    """
    This function performs an I3C TARGET READ MEM command.

    Arguments
    ---------
    id : c_uint16
        ID that identifies the transaction.
    memoryAddress : c_uint16
        Register address of the memory to start reading from.
    length : c_uint16
        Length of the data to be read.

    Returns
    -------
    tuple
        Command list with the commands to be sent to the USB device and the response instance.

    """
    command = I3cTargetTransferMemoryRequest_t()

    command.fields.header.id = id
    command.fields.header.code = I3cCommandCodes.I3C_TARGET_READ_MEMORY.value

    command.fields.parameters.memoryAddress = memoryAddress
    command.fields.parameters.payloadLength = length

    return command.toBytes(), I3cTargetTransferMemoryResponse_t()