from ctypes import *

#================================================================================#
# region USB Packet Header.
#================================================================================#

class UsbTransferPacketHeaderFields_t(Structure):
    """
    USB Transfer Packet Header Fields definition.

    This structures represents the different fields that compose the header of the
    USB packets. It allows to seamlessly access the different fields in order to
    write to them or read from them.
    """
    _pack_ = 1
    _fields_ = [("sot", c_uint16, 1),
                ("eot", c_uint16, 1),
                ("payloadLength", c_uint16, 10),
                ("reserved", c_uint16, 4)]

UsbTransferUsbTransferPacketHeaderArray_t = c_uint8 * sizeof(UsbTransferPacketHeaderFields_t)

class UsbTransferPacketHeader_t(Union):
    """
    USB Transfer Packet Header union definition.

    This union represents the header of the USB packets transferred between the
    USB Host and the USB Host Adapter. This unions allows serialization and
    deserialization of the information by combining the UsbTransferPacketHeaderFields_t
    structure and the UsbTransferUsbTransferPacketHeaderArray_t array.
    """
    _fields_ = [("data", UsbTransferUsbTransferPacketHeaderArray_t),
               ("fields", UsbTransferPacketHeaderFields_t)]

    def toBytes(self) -> bytes:
        return bytes(self.data)

#endregion

#================================================================================#
# region Constants definition
#================================================================================#

USB_FS_INTERRUPT_ENDPOINT_SIZE          = 64
USB_FS_TRANSFER_PACKET_PAYLOAD_LENGTH   = USB_FS_INTERRUPT_ENDPOINT_SIZE - sizeof(UsbTransferPacketHeaderFields_t)

USB_HS_INTERRUPT_ENDPOINT_SIZE          = 1024
USB_HS_TRANSFER_PACKET_PAYLOAD_LENGTH   = USB_HS_INTERRUPT_ENDPOINT_SIZE - sizeof(UsbTransferPacketHeaderFields_t)

#endregion

#================================================================================#
# region USB TRANSFER PROTOCOL class
#================================================================================#

class UsbTransferProtocol:
    """
    Usb Transfer Protocol class in charge of managing the USB Packets transfer.

    This class is intended to control the management of USB packets transferred
    between the USB Host and the USB Host Adapter devices. This class is in total
    aware of the structure of the USB packets and for this reason is able to
    extract the information from incoming packets in order to build the whole input transfer,
    as well as create all the output packets to send data to the USB Host Adapter.

    Attributes
    ----------
    inputTransfer: bytearray
        This bytearray object allows to accumulate the payload of incoming packets in order
        to rebuild the whole input transfer.
    outputTransferPackets: list
        This list object is intended to accumulate all the USB Packets whose payload contains
        a chunk of the complete output transfer.
    endpointSize: int
        Size of the USB interrupt transfer endpoint.

    Methods
    -------
    createUsbOutputTransferPackets(data: bytes)
        Create as many USB packets as needed to transfer data to the USB device.
    receiveUsbInputTransferPackets(data: bytes)
        Receives the input transfer packets sent by the device and creates the whole
        input transfer.

    """

    def __init__(self, endpointSize):

        self.inputTransfer = bytearray()
        self.outputTransferPackets = []
        self.endpointSize = endpointSize

    def createUsbOutputTransferPackets(self, data: bytes) -> list:
        """
        Create as many USB packets as needed to transfer data to the USB device.

        This function receives the whole output transfer data to be sent, create data chunks and build
        as many USB packets as required to transfer the whole data to the device.
        Return a list containing all the packets to be sent to the device.

        Parameters
        ----------
        data: bytes
            A bytes object containing the data to be transferred to the device.

        Returns
        -------
        list
            A list containing all the USB packets.

        """
        self.outputTransferPackets.clear()

        if self.endpointSize == USB_FS_INTERRUPT_ENDPOINT_SIZE:
            packetPayloadLength = USB_FS_TRANSFER_PACKET_PAYLOAD_LENGTH
        elif self.endpointSize == USB_HS_INTERRUPT_ENDPOINT_SIZE:
            packetPayloadLength = USB_HS_TRANSFER_PACKET_PAYLOAD_LENGTH

        nPackets    = len(data) // packetPayloadLength
        nModPackets = len(data) % packetPayloadLength
        if nModPackets != 0: nPackets += 1

        for i in range(nPackets):

            header = UsbTransferPacketHeader_t()

            if i == 0:
                header.fields.sot = 1
            if i == (nPackets - 1):
                header.fields.eot = 1

            startIndex = i * packetPayloadLength
            remainingLength = len(data) - startIndex
            header.fields.payloadLength = min(remainingLength, packetPayloadLength);
            endIndex = startIndex + header.fields.payloadLength

            packet = header.toBytes() + data[startIndex:endIndex]
            self.outputTransferPackets.append(packet)

        return self.outputTransferPackets

    def receiveUsbInputTransferPackets(self, data: bytes) -> bytearray:
        """
        Receives the input transfer packets sent by the device and creates the whole
        input transfer.

        Receives a bytes object containing the serialization of an input transfer packet
        sent by the device. Accumulate the payload of the input packets until the last one is
        received. Returns a bytearray object containing the complete transfer data when the last
        USB packet arrives. Otherwise, returns None.

        Parameters
        ----------
        data: bytes
            A bytes object containing the data sent by the USB device.

        Returns
        -------
        None
            Returns None while an interrupt is still ongoing and the last packet has not been
            received yet.
        bytearray:
            Returns a bytearray object containing all the input transfer sent by the USB device.

        """

        headerLength = sizeof(UsbTransferPacketHeader_t)
        header = UsbTransferPacketHeader_t.from_buffer_copy(data[:headerLength])

        if header.fields.sot:
            self.inputTransfer.clear()


        self.inputTransfer += data[headerLength : headerLength + header.fields.payloadLength]

        if header.fields.eot:
            return self.inputTransfer
        else:
            return None

#endregion