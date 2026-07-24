from ow_ustx import *
import json
import time

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

# SW Trigger setup
#
# TriggerFrequencyHz - trigger frequency in hertz
# TriggerMode CONTINUOUS - will continue pulsing till stopped with stop command
#             PULSECOUNT - Will fire the number of pulses specified
# TriggerPulseCount - number of pulses for trigger, ignored when in CONTINUOUS mode
# TriggerPulseWidthUsec - Trigger pulse width in usec must be less than

# freq supported 2 - 5000 Hz
# TriggerMode is 0 for Continuous trigger and 1 for Pulsed Counted Trigger
# pulsed trigger not supported yet
json_data = {
    "TriggerFrequencyHz": 100,
    "TriggerMode": 0,
    "TriggerPulseCount": 0,
    "TriggerPulseWidthUsec": 500
}

# Send and Recieve USTX 7332         
tx7332 = TX7332(s)

# get current trigger settings
r = tx7332.get_trigger()
print(r)

# set trigger using json
tx7332.set_trigger(json_data)
r = tx7332.get_trigger()
print(r)

reg_values = [
    [0x00, 0x00000000],
    [0x01, 0x00000000],
    [0x06, 0x00000000],
    [0x0B, 0x00000000],
    [0x0C, 0x00000000],
    [0x0F, 0x00000000],
    [0x14, 0x00000000],
    [0x15, 0x00000000],
    [0x16, 0x00000000],
    [0x17, 0x00000000],
    [0x18, 0x02000003],
    [0x19, 0x00000744],
    [0x1A, 0x00000000],
    [0x1B, 0x00000000],
    [0x1E, 0x00000000],
    [0x1F, 0x00000000],
    [0x20, 0x1FFF1770],
    [0x21, 0x1FFF1770],
    [0x22, 0x0E1004B0],
    [0x23, 0x0E1004B0],
    [0x24, 0x1C2012C0],
    [0x25, 0x1C2012C0],
    [0x26, 0x09600000],
    [0x27, 0x09600000],
    [0x28, 0x1FFF1770],
    [0x29, 0x1FFF1770],
    [0x2A, 0x0E1004B0],
    [0x2B, 0x0E1004B0],
    [0x2C, 0x1C2012C0],
    [0x2D, 0x1C2012C0],
    [0x2E, 0x09600000],
    [0x2F, 0x09600000],
    [0x120, 0xF1F2F2F2],
    [0x121, 0x0007F1F1]
]

"""
# Writing to an address
for id in range(1):
    tx7332.write_register(0x00, 0x00000000, id)
    tx7332.write_register(0x01, 0x00000000, id)
    tx7332.write_register(0x06, 0x00000000, id)
    tx7332.write_register(0x0B, 0x00000000, id)
    tx7332.write_register(0x0C, 0x00000000, id)
    tx7332.write_register(0x0F, 0x00000000, id)
    tx7332.write_register(0x14, 0x00000000, id)
    tx7332.write_register(0x15, 0x00000000, id)
    tx7332.write_register(0x16, 0x00000000, id)
    tx7332.write_register(0x17, 0x00000000, id)
    tx7332.write_register(0x18, 0x02000003, id)
    tx7332.write_register(0x19, 0x00000744, id)
    tx7332.write_register(0x1A, 0x00000000, id)
    tx7332.write_register(0x1B, 0x00000000, id)
    tx7332.write_register(0x1E, 0x00000000, id)
    tx7332.write_register(0x1F, 0x00000000, id)
    tx7332.write_register(0x20, 0x1FFF1770, id)
    tx7332.write_register(0x21, 0x1FFF1770, id)
    tx7332.write_register(0x22, 0x0E1004B0, id)
    tx7332.write_register(0x23, 0x0E1004B0, id)
    tx7332.write_register(0x24, 0x1C2012C0, id)
    tx7332.write_register(0x25, 0x1C2012C0, id)
    tx7332.write_register(0x26, 0x09600000, id)
    tx7332.write_register(0x27, 0x09600000, id)
    tx7332.write_register(0x28, 0x1FFF1770, id)
    tx7332.write_register(0x29, 0x1FFF1770, id)
    tx7332.write_register(0x2A, 0x0E1004B0, id)
    tx7332.write_register(0x2B, 0x0E1004B0, id)
    tx7332.write_register(0x2C, 0x1C2012C0, id)
    tx7332.write_register(0x2D, 0x1C2012C0, id)
    tx7332.write_register(0x2E, 0x09600000, id)
    tx7332.write_register(0x2F, 0x09600000, id)

    tx7332.write_register(0x120, 0xF1F2F2F2, id)
    tx7332.write_register(0x121, 0x0007F1F1, id)

# Reading from an address
for id in range(1):
    value = tx7332.read_register(0x20, id)
    print(f'CHIP: {id} 0x20: {value:08X}')
    value = 0
    value = tx7332.read_register(0x120, id)
    print(f'CHIP: {id} 0x20: {value:08X}')

"""

# tx7332.write_demo_config(0)
tx7332.write_block(reg_values, 0)
tx7332.start_trigger()
# GREEN LED should be on

time.sleep(5)  # Pauses for 5 seconds

tx7332.stop_trigger()
# GREEN LED should be off

# Close serial port
s.close()
