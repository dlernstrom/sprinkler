import telnetlib
import time
import re


class Numato:
    def __init__(self, device_ip, username, password):
        self.device_ip = device_ip
        self.username = username
        self.password = password
        # Create a new TELNET object
        self.telnet_obj = telnetlib.Telnet(device_ip)

    def connect(self):
        """Connect to device with user provided credentials"""
        # Wait for login prompt from device and enter user name when prompted
        self.telnet_obj.read_until(b"login")
        self.telnet_obj.write(self.username.encode('ascii') + b"\r\n")

        # Wait for password prompt and enter password when prompted by device
        self.telnet_obj.read_until(b"Password: ")
        self.telnet_obj.write(self.password.encode('ascii') + b"\r\n")

        # Wait for device response
        log_result = self.telnet_obj.read_until(b"successfully\r\n")
        self.telnet_obj.read_until(b">")

        # Check if login attempt was successful
        if b"successfully" in log_result:
            print("\nLogged in successfully... Connected to device", self.device_ip, "\n")
            return True
        elif "denied" in log_result:
            print("Login failed!!!! Please check login credentials or Device IP Address\n\n")
            return False

    def shutdown(self):
        self.telnet_obj.close()

    def flush_buffer(self):
        """Flush any data that may be left in the input buffer"""
        self.telnet_obj.read_eager()

    @staticmethod
    def convert_relay_number(relay_number):
        """Converts the relay_number(A to V) to upper case if user entered it as lower case."""
        if re.match("^[a-v]*$", relay_number):
            relay_number = relay_number.upper()
        return relay_number

    def relay_on(self, relay_number):
        """Turns the relay on"""
        relay_number = await self.convert_relay_number(relay_number)
        self.telnet_obj.write(("relay on " + str(relay_number) + "\r\n").encode())
        print("Relay ON", relay_number)
        time.sleep(1)
        self.telnet_obj.read_eager()
        self.relay_read(relay_number)

    def relay_off(self, relay_number):
        """Turns the relay off"""
        self.telnet_obj.write(("relay off " + str(relay_number) + "\r\n").encode())
        print("Relay OFF", relay_number)
        time.sleep(1)
        self.telnet_obj.read_eager()
        self.relay_read(relay_number)

    def relay_read(self, relay_number):
        """Reads and returns the state of the relay"""
        self.telnet_obj.write(b"relay read " + str(relay_number).encode("ascii") + b"\r\n")
        time.sleep(1)
        response = self.telnet_obj.read_eager()
        readable_response = re.split(br'[&>]', response)[0].decode()
        print("\nRelay read", relay_number, ":", readable_response)
        return readable_response
