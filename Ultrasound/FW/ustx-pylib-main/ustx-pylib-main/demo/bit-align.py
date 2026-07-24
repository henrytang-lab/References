import sys
sys.path.append('.././USTX-PYLIB/')

from ow_ustx import *
import json

def test_bit_align(port='COM23', baudrate=921600, align=8):
    # Select communication port
    s = UART(port, baud_rate=baudrate, timeout=10, align=align)

    # Send and Recieve USTX ping command
    r = s.send_ustx(1, OW_CMD, USTX_PING)
    s.clear_buffer()
        
    # Format and print the received data in hex format
    format_and_print_hex(r)
    
    # Send and Recieve USTX version command
    r = s.send_ustx(2, OW_CMD, USTX_VERSION)
    s.clear_buffer()
    try:
        retPacket = UartPacket(buffer=r)
        print(f"Firmware Version {retPacket.data[0]}.{retPacket.data[1]}.{retPacket.data[2]}")
    except Exception as e:
        print("Error decoding JSON:", e)
    
    # Send and Recieve USTX ID command
    r = s.send_ustx(3, OW_CMD, USTX_ID)
    s.clear_buffer()
    format_and_print_hex(r)
    
    r = s.send_ustx(4, OW_CMD, USTX_ECHO)
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



if __name__ == "__main__":
    test_bit_align()
