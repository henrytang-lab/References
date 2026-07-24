
from .core import *
from .config import *
import struct

class TX7332:
    def __init__(self, uart: UART):
        """
        Initialize the Tx7332 class with an instance of UART.

        :param uart: Instance of the UART class for communication.
        """
        self.uart = uart

    def write_register(self, address: int, value: int, index: int = 0):
        """
        Write a 32-bit value to a 16-bit address.

        :param address: The 16-bit address where the value will be written.
        :param value: The 32-bit value to write.
        :param index: The tx chip index (0-3) to target. Default is 0.        
        """
        if not (0 <= index <= 3):
            raise ValueError("Chip address must be in the range 0-3")
        
        # Prepare data payload
        data = struct.pack('<I', value)
        print(data)
        # Send USTX_WRITE7332 command with data
        self.uart.send_ustx(id=index, packetType=OW_TX7332, command=CMD_WRITE_ADDR, data=data)
        # handle response check for error raise exception on error

        # clear buffer
        self.uart.clear_buffer()

    def read_register(self, address: int, index: int = 0):
        """
        Read a 32-bit value from a 16-bit address.

        :param address: The 16-bit address to read from.
        :param index: The tx chip index (0-3) to target. Default is 0.      
        :return: The 32-bit value read from the address.  
        """
        if not (0 <= index <= 3):
            raise ValueError("Chip address must be in the range 0-3")
        
        # Prepare data payload
        data = address.to_bytes(2, 'big')

        # Send USTX_READ7332 command with data
        response = self.uart.send_ustx(id=index, packetType=OW_TX7332, command=CMD_READ_ADDR, data=data)

        # handle response
        ret_val = 0
        try:
            retPacket = UartPacket(buffer=response)
            if retPacket.data_len == 4:
                ret_val = struct.unpack('<I', retPacket.data)[0]

        except Exception as e:
            print("Error reading response:", e)
        # clear buffer
        self.uart.clear_buffer()

        # Assuming the response contains the 32-bit value right after the header
        # Extract and return the 32-bit value
        # return int.from_bytes(response[header_length:], 'big')
        return ret_val

    def write_block(self, regdat, index: int = 0):
        if not (0 <= index <= 3):
            raise ValueError("Chip address must be in the range 0-3")
        
        # Prepare data payload
        data = bytearray()
        for idx in regdat:
            data.extend(idx[0].to_bytes(4, 'big'))
            data.extend(idx[1].to_bytes(4, 'big'))

        # Send USTX_WRITE7332 command with data
        response = self.uart.send_ustx(id=index, packetType=OW_TX7332, command=CMD_WRITE_BLOCK, data=data)
        # handle response check for error raise exception on error
        print(response)

        # clear buffer
        self.uart.clear_buffer()

    def start_trigger(self):
        # Prepare data payload
        # Send USTX_WRITE7332 command with data
        self.uart.send_ustx(id=1, packetType=OW_TX7332, command=CMD_START_SWTRIG, data=None)
        # handle response

        # clear buffer
        self.uart.clear_buffer()

    def stop_trigger(self):
        # Prepare data payload
        # Send USTX_WRITE7332 command with data
        self.uart.send_ustx(id=1, packetType=OW_TX7332, command=CMD_STOP_SWTRIG, data=None)
        # handle response

        # clear buffer
        self.uart.clear_buffer()

    def write_demo_config(self, index: int = 0):
        # Prepare data payload
        # Send USTX_WRITE7332 command with data
        self.uart.send_ustx(id=index, packetType=OW_TX7332, command=CMD_WRITE_DEMO, data=None)
        # handle response

        # clear buffer
        self.uart.clear_buffer()

    def verify_demo_config(self, index: int = 0):
        # Prepare data payload
        # Send USTX_WRITE7332 command with data
        self.uart.send_ustx(id=index, packetType=OW_TX7332, command=CMD_VERIFY_DEMO, data=None)
        # handle response

        # clear buffer
        self.uart.clear_buffer()

    def set_trigger(self, data = None):
        # Prepare data payload        
        if data:
            try:
                json_string = json.dumps(data)
            except json.JSONDecodeError as e:
                # Handle the error if data is not valid JSON
                print(f"Data must be valid JSON: {e}")
                return  

            payload = json_string.encode('utf-8')
        else:
            payload = None # assume a byte buffer

        # Send Set Trigger command
        self.uart.send_ustx(id=1, packetType=OW_TX7332, command=CMD_SET_SWTRIG, data=payload)
        # handle response

        # clear buffer
        self.uart.clear_buffer()

    def get_trigger(self):
        # Prepare data payload        
        # Send Get Trigger command
        response = self.uart.send_ustx(id=1, packetType=OW_TX7332, command=CMD_GET_SWTRIG, data=None)
        # handle response
        data_object = None
        try:
            retPacket = UartPacket(buffer=response)
            data_object = json.loads(retPacket.data.decode('utf-8'))
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)

        # clear buffer
        self.uart.clear_buffer()
        return data_object