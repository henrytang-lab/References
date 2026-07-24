import unittest
from ow_ustx import *
import json

class TestCoreFunctions(unittest.TestCase):
    def test_all(self):
        # Select communication port
        s = UART('COM24')

        # Send and Recieve USTX ping command
        r = s.send_ustx(1, OW_CMD, USTX_PING)
        s.clear_buffer()
            
        # Format and print the received data in hex format
        format_and_print_hex(r)
        
        # Send and Recieve USTX version command
        r = s.send_ustx(2, OW_CMD, USTX_VERSION)
        s.clear_buffer()
        format_and_print_hex(r)
        
        for i in range(10): 
            # Send and Recieve USTX ID command
            r = s.send_ustx(3, OW_CMD, USTX_ID)
            s.clear_buffer()
            format_and_print_hex(r)
        
        r = s.send_ustx(3, OW_CMD, USTX_ECHO)
        s.clear_buffer()
        format_and_print_hex(r)

        # Create the JSON structure
        json_data = {
            "temperature": 23.5,
            "humidity": 45.6,
            "status": "OK"
        }

        # Send and Recieve JSON command
        r = s.send_ustx(4, OW_JSON, USTX_ECHO, json_data)
        s.clear_buffer()
        format_and_print_hex(r)
        try:
            retPacket = UartPacket(buffer=r)
            data_object = json.loads(retPacket.data.decode('utf-8'))
            print(data_object)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        # Close serial port
        s.close()

        # Send and Recieve USTX 7332         
        tx7332 = TX7332(s)

        # Writing to an address
        tx7332.write_register(0x20, 0x1FFF1770)
            
        # Reading from an address
        value = tx7332.read_register(0x20)
        print('0x20: 0x{:08X}'.format(value))

if __name__ == "__main__":
    unittest.main()
