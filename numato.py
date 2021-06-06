"""Low level handler to the Numato relay device"""
import logging
import telnetlib
import time
import re

from constants import NUMATO_IP, NUMATO_USER, NUMATO_PASS
from exceptions import NumatoError, LoginError

logger = logging.getLogger(__name__)


class Numato:
    def __init__(self):
        self.device_ip = NUMATO_IP
        self.username = NUMATO_USER
        self.password = NUMATO_PASS
        self.telnet_obj = telnetlib.Telnet(NUMATO_IP)
        self.connect()

    def connect(self):
        """Connect to device with user provided credentials"""
        # Wait for login prompt from device and enter user name when prompted
        self.telnet_obj.read_until(b"login")
        self.telnet_obj.write(f'{self.username}\r\n'.encode())

        # Wait for password prompt and enter password when prompted by device
        self.telnet_obj.read_until(b"Password: ")
        self.telnet_obj.write(f'{self.password}\r\n'.encode())

        # Wait for device response
        log_result = self.telnet_obj.read_until(b"successfully\r\n")
        self.telnet_obj.read_until(b">")

        # Check if login attempt was successful
        if b"successfully" in log_result:
            logger.info("Logged in successfully... Connected to device %s", self.device_ip)
            return True
        elif b"denied" in log_result:
            logger.critical("Login failed!!!! Please check login credentials or Device IP Address")
            raise LoginError('Problem logging into device')
        raise NumatoError('Some other problem occurred during login')

    def shutdown(self):
        """Disconnects the telnet object"""
        self.telnet_obj.close()
        self.telnet_obj = None

    def flush_buffer(self):
        """Flush any data that may be left in the input buffer"""
        self.telnet_obj.read_eager()

    @staticmethod
    def convert_relay_number(relay_number):
        """Converts the relay_number(A to V) to upper case if user entered it as lower case."""
        if re.match("^[a-v]*$", relay_number):
            relay_number = relay_number.upper()
        return relay_number

    def reconnect(self):
        """Shutdown and reconnect, typically because we had a BrokenPipeError"""
        logger.warning('Lost connection, reconnecting')
        self.shutdown()
        self.connect()

    def relay_on(self, relay_number):
        """Turns the relay on, reconnecting if necessary"""
        try:
            self._relay_on_engine(relay_number)
        except BrokenPipeError:
            self.reconnect()
            self._relay_on_engine(relay_number)

    def _relay_on_engine(self, relay_number):
        """Turns the relay on"""
        # relay_number = self.convert_relay_number(relay_number)
        logger.info('Turning relay ON: %s', relay_number)
        readable_response = self._send_command_fetch_response(f'relay on {relay_number}\r\n')
        logger.info('Command Response: [%s]', readable_response)
        self.relay_read(relay_number)

    def relay_off(self, relay_number):
        """Turns the relay off, reconnecting if necessary"""
        try:
            self._relay_off_engine(relay_number)
        except BrokenPipeError:
            self.reconnect()
            self._relay_off_engine(relay_number)

    def _relay_off_engine(self, relay_number):
        """Turns the relay off"""
        logger.info('Turning relay OFF: %s', relay_number)
        readable_response = self._send_command_fetch_response(f'relay off {relay_number}\r\n')
        logger.info('Command Response: [%s]', readable_response)
        self.relay_read(relay_number)

    def relay_read(self, relay_number):
        """Reads and returns the state of the relay, reconnecting if necessary"""
        try:
            self._relay_read_engine(relay_number)
        except BrokenPipeError:
            self.reconnect()
            self._relay_read_engine(relay_number)

    def _relay_read_engine(self, relay_number):
        """Reads and returns the state of the relay"""
        logger.info('Reading relay state: %s', relay_number)
        readable_response = self._send_command_fetch_response(f'relay read {relay_number}\r\n')
        logger.info('Command Response: [%s]', readable_response)
        return readable_response

    def _send_command_fetch_response(self, command):
        self.telnet_obj.write(command.encode())
        time.sleep(1)
        response = self.telnet_obj.read_eager().decode().strip()
        return re.split(r'[&>]', response)[0]
