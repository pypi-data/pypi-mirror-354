"""WHAD new hardware interface
"""
import logging
import contextlib
from time import time, sleep
from typing import Generator, Callable
from threading import Thread, Lock
from queue import Queue, Empty

from whad.exceptions import WhadDeviceNotReady, WhadDeviceError, \
    WhadDeviceTimeout, WhadDeviceDisconnected, WhadDeviceNotFound
from whad.hub import ProtocolHub
from whad.hub.message import HubMessage
from whad.helpers import message_filter
from whad.hub.generic.cmdresult import CommandResult, ResultCode
from whad.hub.discovery import InfoQueryResp, DomainInfoQueryResp, DeviceReady
from whad.hub.discovery import DeviceType
from whad.device.info import WhadDeviceInfo

logger = logging.getLogger(__name__)

class IfaceEvt:
    """Interface event.
    """
    def __init__(self, iface = None):
        self.__iface = iface

    def __repr__(self) -> str:
        """Printable representation of this event
        """
        return f"IfaceEvt(iface='{self.__iface.name}')"

class Disconnected(IfaceEvt):
    """Interface has disconnected.
    """
    def __repr__(self) -> str:
        """Printable representation of this event.
        """
        return f"DisconnectedEvt(iface='{self.__iface.name}')"

class MessageReceived(IfaceEvt):
    """Message has been received.
    """
    def __init__(self, iface = None, message = None):
        super().__init__(iface)
        self.__message = message

    @property
    def message(self) -> HubMessage:
        """Received message."""
        return self.__message

    def __repr__(self) -> str:
        """Printable representation of this event.
        """
        return f"WhadMessageReceived(iface='{self.__iface.name}')"

class IfaceInThread(Thread):
    """Internal thread processing data sent by the connector to the
    hardware interface.
    """

    def __init__(self, iface = None):
        super().__init__()
        self.__iface = iface
        self.__canceled = False

    def cancel(self):
        """Cancel thread
        """
        self.__canceled = True

    def serialize(self, message) -> bytes:
        """Serialize a WHAD message.
        """
        # Serialize protobuf message
        raw_msg = message.serialize()

        # Define header
        header = [
            0xAC, 0xBE,
            len(raw_msg) & 0xff,
            (len(raw_msg) >> 8) & 0xff
        ]

        # Build the final payload
        return bytes(header) + raw_msg

    def run(self):
        """Out thread main task.
        """
        while not self.__canceled:
            # Read data from device (may block)
            try:
                # Wait for a message to send to interface (blocking)
                logger.debug("[in_thread] waiting for message to send")
                with self.__iface.get_pending_message(timeout=1.0) as message:
                    logger.debug("[in_thread] sending message %s", message)
                    # Serialize message and send it.
                    payload = self.serialize(message)

                    # Send serialized message to interface
                    logger.debug("[in_thread] acquiring lock on interface ...")
                    self.__iface.lock()
                    logger.debug("[in_thread] sending payload %s ...", payload)
                    self.__iface.write(payload)
                    logger.debug("[in_thread] releasing lock ...")
                    self.__iface.unlock()

                    # Notify message has correctly been sent, from a dedicated
                    # thread.
                    if message.has_callback():
                        Thread(target=message.sent).start()
            except Empty:
                pass
            except WhadDeviceNotReady:
                if message.has_callback():
                    Thread(target=message.error, args=[1]).start()
                break
            except WhadDeviceDisconnected:
                if message.has_callback():
                    Thread(target=message.error, args=[2]).start()
                break

class IfaceOutThread(Thread):
    """Internal thread processing data sent by the hardware interface
    to the interface object.
    """
    def __init__(self, iface = None):
        super().__init__()
        self.__iface = iface
        self.__canceled = False

        # Data processing
        self.__data = bytearray()

    def cancel(self):
        """Cancel thread
        """
        self.__canceled = True

    def ingest(self, data: bytes):
        """Ingest incoming bytes.
        """
        self.__data.extend(data)
        while len(self.__data) > 2:
            # Is the magic correct ?
            if self.__data[0] == 0xAC and self.__data[1] == 0xBE:
                # Have we received a complete message ?
                if len(self.__data) > 4:
                    msg_size = self.__data[2] | (self.__data[3] << 8)
                    if len(self.__data) >= (msg_size+4):
                        raw_message = self.__data[4:4+msg_size]

                        # Parse received message with our Protocol Hub
                        msg = self.__iface.hub.parse(bytes(raw_message))

                        # Forward message if successfully parsed
                        if msg is not None:
                            self.__iface.put_message(msg)

                        # Chomp
                        self.__data = self.__data[msg_size + 4:]
                    else:
                        break
                else:
                    break
            else:
                # Nope, that's not a header
                while len(self.__data) >= 2:
                    if (self.__data[0] != 0xAC) or (self.__data[1] != 0xBE):
                        self.__data = self.__data[1:]
                    else:
                        break

    def run(self):
        """Out thread main task.
        """
        while not self.__canceled:
            # Read data from device (may block)
            try:
                data = self.__iface.read()
                if data is not None:
                    self.ingest(data)
            except WhadDeviceNotReady:
                break
            except WhadDeviceDisconnected:
                break

class Interface:
    """WHAD 'new' hardware interface.
    """
    INTERFACE_NAME = None

    @classmethod
    def _get_sub_classes(cls):
        """
        Helper allowing to get every subclass of WhadDevice.
        """
        # List every available device class
        device_classes = set()
        for device_class in cls.__subclasses__():
            if device_class.__name__ == "VirtualDevice":
                for virtual_device_class in device_class.__subclasses__():
                    device_classes.add(virtual_device_class)
            else:
                device_classes.add(device_class)
        return device_classes

    @classmethod
    def create_inst(cls, interface_string):
        """
        Helper allowing to get a device according to the interface string provided.

        To make it work, every device class must implement:
            - a class attribute INTERFACE_NAME, matching the interface name
            - a class method list, returning the available devices
            - a property identifier, allowing to identify the device in a unique way

        This method should NOT be used outside of this class. Use WhadDevice.create instead.
        """

        if interface_string.startswith(cls.INTERFACE_NAME):
            identifier = None
            index = None
            if len(interface_string) == len(cls.INTERFACE_NAME):
                index = 0
            elif interface_string[len(cls.INTERFACE_NAME)] == ":":
                index = None
                try:
                    _, identifier = interface_string.split(":")
                except ValueError:
                    identifier = None
            else:
                try:
                    index = int(interface_string[len(cls.INTERFACE_NAME):])
                except ValueError:
                    index = None

            # Retrieve the list of available devices
            # (could be a list or a dict)
            available_devices = cls.list()

            # If the list of device is built statically, check before instantiation
            if available_devices is not None:
                if index is not None:
                    try:
                        # Try to retrieve a device based on the provided index
                        return available_devices[index]
                    except KeyError as exc:
                        raise WhadDeviceNotFound from exc
                    except IndexError as exc:
                        raise WhadDeviceNotFound from exc
                elif identifier is not None:
                    if isinstance(available_devices, list):
                        for dev in available_devices:
                            if dev.identifier == identifier:
                                return dev
                    elif isinstance(available_devices, dict):
                        for dev_id, dev in available_devices.items():
                            if dev.identifier == identifier:
                                return dev
                    raise WhadDeviceNotFound
                else:
                    raise WhadDeviceNotFound
            # Otherwise, check dynamically using check_interface
            else:
                formatted_interface_string = interface_string.replace(
                    cls.INTERFACE_NAME + ":",
                    ""
                )
                if cls.check_interface(formatted_interface_string):
                    return cls(formatted_interface_string)
                raise WhadDeviceNotFound

        else:
            raise WhadDeviceNotFound

    @classmethod
    def create(cls, interface_string):
        '''
        Create a specific device according to the provided interface string,
        formed as follows:

        <device_type>[device_index][:device_identifier]

        Examples:
            - `uart` or `uart0`: defines the first compatible UART device available
            - `uart1`: defines the second compatible UART device available
            - `uart:/dev/ttyACMO`: defines a compatible UART device identified by `/dev/tty/ACMO`
            - `ubertooth` or `ubertooth0`: defines the first available Ubertooth device
            - `ubertooth:11223344556677881122334455667788`: defines a Ubertooth device with serial number *11223344556677881122334455667788*
        '''
        device_classes = cls._get_sub_classes()

        device = None
        for device_class in device_classes:
            try:
                device = device_class.create_inst(interface_string)
                return device
            except WhadDeviceNotFound:
                continue

        raise WhadDeviceNotFound

    @classmethod
    def list(cls):
        '''
        Returns every available compatible devices.
        '''
        device_classes = cls._get_sub_classes()

        available_devices = []
        for device_class in device_classes:
            device_class_list = device_class.list()
            if device_class_list is not None:
                if isinstance(device_class_list, list):
                    for device in device_class_list:
                        available_devices.append(device)
                elif isinstance(device_class_list, dict):
                    for dev_id, device in device_class_list.items():
                        available_devices.append(device)
        return available_devices

    @classmethod
    def check_interface(cls, interface):
        '''
        Checks dynamically if the device can be instantiated.
        '''
        logger.debug("default: checking interface %s fails.", interface)
        return False

    @property
    def interface(self):
        '''
        Returns the current interface of the device.
        '''
        # If class has interface name, return the interface alias
        if hasattr(self.__class__,"INTERFACE_NAME"):
            return self.__class__.INTERFACE_NAME + str(self.index)

        # Interface is unknown
        return "unknown"

    @property
    def type(self):
        '''
        Returns the name of the class linked to the current device.
        '''
        return self.__class__.__name__

    def __init__(self, index: int = None):
        """Initialize an interface
        """
        # Interface state
        self.__info = None
        self.__opened = False
        self.__discovered = False
        self.__closing = False

        # Generate device index if not provided
        if index is None:
            self.inc_dev_index()
            self.__index = self.__class__.CURRENT_DEVICE_INDEX
        else:
            # Used by HCI devices to force index to match system names
            self.__index = index

        # IO Threads
        self.__iface_in = None
        self.__iface_out = None

        # Queue holding messages from connector, waiting to be sent to
        # the interface.
        self.__in_messages = Queue()

        # Queue holding messages from interface, waiting to be sent to
        # an attached connector
        self.__out_messages = Queue()

        # Connector bound to this device
        self.__connector = None

        # Interface lock
        self.__lock = Lock()

        # Connector lock
        self.__msg_filter: Callable[..., bool] = None

        # Protocol hub
        self.__hub = ProtocolHub()

        # Communication timeout
        self.__timeout = 5.0

    @contextlib.contextmanager
    def get_pending_message(self, timeout: float = None) -> Generator[HubMessage, None, None]:
        """Get message waiting to be sent to the interface.
        """
        try:
            yield self.__in_messages.get(timeout=timeout)
        except Empty as err:
            raise err
        else:
            self.__in_messages.task_done()

    @property
    def connector(self):
        """Connector bound to the interface
        """
        return self.__connector

    @property
    def hub(self):
        """Retrieve the device protocol hub (parser/factory)
        """
        return self.__hub

    @property
    def index(self) -> int:
        """Get the interface index

        :return: Interface index
        :rtype: int
        """
        return self.__index

    @property
    def device_id(self):
        """Return device ID
        """
        return self.__info.device_id

    @property
    def info(self) -> WhadDeviceInfo:
        """Get device info object

        :return: Device information object
        :rtype: WhadDeviceInfo
        """
        return self.__info

    @property
    def opened(self) -> bool:
        """Device is open ?
        """
        return self.is_open()

    def is_open(self) -> bool:
        """Determine if interface is opened.
        """
        return self.__opened

    @classmethod
    def inc_dev_index(cls):
        """Inject and maintain device index.
        """
        if hasattr(cls, 'CURRENT_DEVICE_INDEX'):
            cls.CURRENT_DEVICE_INDEX += 1
        else:
            cls.CURRENT_DEVICE_INDEX = 0

    def set_connector(self, connector):
        """Set interface connector.
        """
        self.__connector = connector

    def lock(self):
        """Lock interface for read/write operation.
        """
        self.__lock.acquire()
        logger.debug("Lock acquired !")

    def unlock(self):
        """Unlock interface for read/write operation.
        """
        logger.debug("Releasing lock ...")
        self.__lock.release()

    def __start_io_threads(self):
        """Start background IO threads
        """
        self.__iface_in = IfaceInThread(self)
        self.__iface_in.start()
        self.__iface_out= IfaceOutThread(self)
        self.__iface_out.start()

    def __stop_io_threads(self):
        """Stop background IO threads
        """
        if self.__iface_in is not None:
            self.__iface_in.cancel()
            self.__iface_in.join()
        if self.__iface_out is not None:
            self.__iface_out.cancel()
            self.__iface_out.join()

    ##
    # Device specific methods
    ##

    def open(self):
        """Handle device open
        """
        # Create interface I/O threads and start them.
        self.__start_io_threads()

        # Ask interface for a reset
        try:
            logger.info("resetting interface (if possible)")
            self.__opened = True
            self.reset()
        except Empty as err:
            # Device is unresponsive, shutdown IO threads
            self.__stop_io_threads()

            raise WhadDeviceNotReady() from err

    def read(self) -> bytes:
        """Read bytes from interface (blocking).
        """
        return b''

    def write(self, payload: bytes) -> int:
        """Write payload to interface.
        """
        return len(payload)

    def close(self):
        """Close device
        """
        logger.info("closing WHAD interface")
        self.__closing = True

        # Cancel I/O thread if required
        self.__stop_io_threads()

        self.__opened = False
        self.__closing = False

        # Notify connector that device has closed
        if self.__connector is not None:
            self.__connector.send_event(Disconnected(self))

    def change_transport_speed(self, speed):
        """Set device transport speed.

        Optional.
        """

    ##
    # Message processing
    ##

    def set_queue_filter(self, keep: Callable[..., bool] = None):
        """Set message queue filter.
        """
        self.__msg_filter = keep

    def put_message(self, message: HubMessage):
        """Process incoming message.
        """
        # If no connector is attached to the interface, redirect to a dedicated
        # message queue.
        if self.__connector is None:
            self.__out_messages.put(message)

        # If a connector is attached to the interface but a message filter
        # is set, redirect matching messages to a dedicated message queue
        # and notify the connector about the other messages.
        elif self.__msg_filter is not None and self.__msg_filter(message):
            self.__out_messages.put(message)
        else:
            self.connector.send_event(MessageReceived(self, message))


    def wait_for_single_message(self, timeout: float = None ,
                                msg_filter: Callable[..., bool] = None):
        """Configures the device message queue filter to automatically move messages
        that matches the filter into the queue, and then waits for the first message
        that matches this filter and returns it.
        """
        unexpected_messages = []
        if msg_filter is not None:
            self.set_queue_filter(msg_filter)

        # Wait for a matching message to be caught (blocking)
        msg = self.__out_messages.get(block=True, timeout=timeout)

        # If message filter is set and message does not match, wait until an
        # expected message matches
        if msg_filter is not None:
            # Wait for a matching message
            while not msg_filter(msg):
                unexpected_messages.append(msg)
                msg = self.__out_messages.get(block=True, timeout=timeout)

            # Re-enqueue non-matching messages
            for m in unexpected_messages:
                self.__out_messages.put(m)
        return msg


    def wait_for_message(self, timeout: float = None, msg_filter: Callable[..., bool] = None,
                         command: bool = False):
        """
        Configures the device message queue filter to automatically move messages
        that matches the filter into the queue, and then waits for the first message
        that matches this filter and process it.

        This method is blocking until a matching message is received.

        :param int timeout: Timeout
        :param filter: Message queue filtering function (optional)
        """

        # Check if device is still opem
        if not self.__opened and self.__out_messages.empty():
            raise WhadDeviceDisconnected()

        logger.debug("entering wait_for_message ...")
        if msg_filter is not None:
            self.set_queue_filter(msg_filter)

        start_time = time()

        while True:
            try:
                # Wait for a matching message to be caught (blocking)
                msg = self.__out_messages.get(block=True, timeout=timeout)

                # If message does not match, re-enqueue
                if not self.__msg_filter(msg):
                    self.put_message(msg)
                    logger.debug("exiting wait_for_message ...")
                else:
                    logger.debug("exiting wait_for_message ...")
                    return msg
            except Empty as err:
                # Queue is empty, wait for a message to show up.
                if timeout is not None and (time() - start_time > timeout):
                    if command:
                        raise WhadDeviceTimeout("WHAD device did not answer to a command") from err

                    logger.debug("exiting wait_for_message ...")
                    return None

    def send_message(self, message: HubMessage, keep: Callable[..., bool] = None):
        """
        Serializes a message and sends it to the interface, without waiting
        for an answer. Optionally, you can update the message queue filter
        if you need to wait for specific messages after the message is sent.

        :param Message message: Message to send
        :param keep: Message queue filter function
        """
        if not self.__opened and self.__out_messages.empty():
            raise WhadDeviceDisconnected()

        # Set message queue filter
        if keep is not None:
            self.set_queue_filter(keep)

        # Enqueue message to transmit to the interface
        self.__in_messages.put(message)


    def send_command(self, command: HubMessage, keep: Callable[..., bool] = None):
        """
        Sends a command and awaits a specific response from the device.
        WHAD commands usualy expect a CmdResult message, if `keep` is not
        provided then this method will by default wait for a CmdResult.

        :param Message command: Command message to send to the device
        :param keep: Message queue filter function (optional)
        :returns: Response message from the device
        :rtype: Message
        """
        # If a queue filter is not provided, expect a default CmdResult
        try:
            if keep is None:
                self.send_message(command, message_filter(CommandResult))
            else:
                self.send_message(command, keep)
        except WhadDeviceError as error:
            # Device error has been triggered, it looks like our device is in
            # an unspecified state, notify user.
            logger.debug("WHAD device in error while sending message: %s", error)
            raise error

        try:
            result = self.wait_for_message(self.__timeout, command=True)
        except WhadDeviceTimeout as timedout:
            # Forward exception
            raise timedout

        # Log message
        logger.debug("Command result: %s", result)

        return result

    ##
    # Interface management
    ##

    ######################################
    # Generic discovery
    ######################################

    def on_discovery_msg(self, message):
        """
        Method called when a discovery message is received. If a connector has
        been associated with the device, forward this message to this connector.
        """

        # Forward everything to the connector, if any
        if self.__connector is not None:
            self.__connector.on_discovery_msg(message)

    def has_domain(self, domain) -> bool:
        """Checks if device supports a specific domain.

        :param Domain domain: Domain
        :returns: True if domain is supported, False otherwise.
        :rtype: bool
        """
        if self.__info is not None:
            return self.__info.has_domain(domain)

        # No info available on device, domain is not supported by default
        return False


    def get_domains(self) -> dict:
        """Get device' supported domains.

        :returns: list of supported domains
        :rtype: list
        """
        if self.__info is not None:
            return self.__info.domains

        # No domain discovered yet
        return {}


    def get_domain_capability(self, domain):
        """Get a device domain capabilities.

        :param Domain domain: Target domain
        :returns: Domain capabilities
        :rtype: DeviceDomainInfoResp
        """
        if self.__info is not None:
            return self.__info.get_domain_capabilities(domain)

        # No capability if not discovered
        return 0

    def get_domain_commands(self, domain):
        """Get a device supported domain commands.

        :param Domain domain: Target domain
        :returns: Bitmask of supported commands
        :rtype: int
        """
        if self.__info is not None:
            return self.__info.get_domain_commands(domain)

        # No supported commands by default
        return 0


    def send_discover_info_query(self, proto_version=0x0100):
        """
        Sends a DeviceInfoQuery message and awaits for a DeviceInfoResp
        answer.
        """
        def discover_info_query_sent(message, status):
            print("Discover info query sent !")

        logger.info("preparing a DeviceInfoQuery message")
        msg = self.__hub.discovery.create_info_query(proto_version)
        msg.callback(discover_info_query_sent)
        return self.send_command(
            msg,
            message_filter(InfoQueryResp)
        )


    def send_discover_domain_query(self, domain):
        """
        Sends a DeviceDomainQuery message and awaits for a DeviceDomainResp
        answer.
        """
        logger.info("preparing a DeviceDomainInfoQuery message")
        msg = self.__hub.discovery.create_domain_query(domain)
        return self.send_command(
            msg,
            message_filter(DomainInfoQueryResp)
        )

    def discover(self):
        """
        Performs device discovery (synchronously).

        Discovery process asks the device to provide its description, including
        its supported domains and associated capabilities. For each domain we
        then query the device and get the list of supported commands.
        """
        if not self.__discovered:
            # We send a DeviceInfoQuery message to the device and expect a
            # DeviceInfoResponse in return.
            resp = self.send_discover_info_query()

            # If we have an answer, process it.
            if resp is not None:

                # Ensure response is the one we expect
                assert isinstance(resp, InfoQueryResp)

                # Save device information
                self.__info = WhadDeviceInfo(
                    resp
                )

                # Parse DeviceInfoResponse
                #device_info = self.hub.parse(resp)

                # Update our ProtocolHub version to the device version
                self.__hub = ProtocolHub(resp.proto_min_ver)

                # Query device domains
                logger.info("query supported commands per domain")
                for domain in self.__info.domains:
                    resp = self.send_discover_domain_query(domain)
                    self.__info.add_supported_commands(
                        resp.domain,
                        resp.supported_commands
                    )

                # Mark device as discovered
                logger.info("device discovery done")
                self.__discovered = True

                # Switch to max transport speed
                logger.info("set transport speed to %d", self.info.max_speed)
                self.change_transport_speed(
                    self.info.max_speed
                )
            else:
                logger.error("device is not ready !")
                raise WhadDeviceNotReady()

    def reset(self):
        """Reset device
        """
        logger.info("preparing a DeviceResetQuery message")
        msg = self.__hub.discovery.create_reset_query()
        return self.send_command(
            msg,
            message_filter(DeviceReady)
        )

class VirtualInterface(Interface):
    """
    Virtual interface implementation.
    
    This variant of the base Interface class provides a way to emulate an interface
    compatible with WHAD. This emulated compatible interface is used as an adaptation
    layer between WHAD's core and third-party hardware that does not run a WHAD-enabled
    firmware.
    """
    def __init__(self, index: int = None):
        self._dev_type = None
        self._dev_id = None
        self._fw_author = None
        self._fw_url = None
        self._fw_version = (0, 0, 0)
        self._dev_capabilities = {}
        self.__lock = Lock()
        super().__init__(index)

    def send_message(self, message, keep=None):
        """Send message to host.
        """
        with self.__lock:
            super().set_queue_filter(keep)
            self._on_whad_message(message)

    def _on_whad_message(self, message):
        """TODO: associate callbacks with classes ?
        """
        category = message.message_type
        message_type = message.message_name

        callback_name = f"_on_whad_{category}_{message_type}"
        if hasattr(self, callback_name) and callable(getattr(self, callback_name)):
            getattr(self, callback_name)(message)
        else:
            logger.info("unhandled message: %s", message)
            self._send_whad_command_result(ResultCode.ERROR)

    def _on_whad_discovery_info_query(self, message):
        major, minor, revision = self._fw_version
        msg = self.hub.discovery.create_info_resp(
            DeviceType.VirtualDevice,
            self._dev_id,
            0x0100,
            0,
            self._fw_author,
            self._fw_url,
            major, minor, revision,
            [domain | (capabilities[0] & 0xFFFFFF) for domain, capabilities in self._dev_capabilities.items()]
        )
        self._send_whad_message(msg)

    def _on_whad_discovery_domain_query(self, message):
        # Compute supported commands for domain
        commands = 0
        supported_commands = self._dev_capabilities[message.domain][1]
        for command in supported_commands:
            commands |= (1 << command)

        # Create a DomainResp message and send it
        msg = self.hub.discovery.create_domain_resp(
            message.domain,
            commands
        )
        self._send_whad_message(msg)


    def _send_whad_message(self, message):
        self.put_message(message)

    def _send_whad_command_result(self, code):
        msg = self.hub.generic.create_command_result(code)
        self._send_whad_message(msg)
