from ow_ustx import *
import argparse
import json
import time


# List of register addresses and expected values
test_config_values = [
    (0x00, 0x00000000),
    (0x01, 0x00000000),
    (0x06, 0x00000000),
    (0x0B, 0x00000000),
    (0x0C, 0x00000000),
    (0x0F, 0x00000000),
    (0x14, 0x00000000),
    (0x15, 0x00000000),
    (0x16, 0x00000000),
    (0x17, 0x00000000),
    (0x18, 0x02000003),
    (0x19, 0x00000744),
    (0x1A, 0x00000000),
    (0x1B, 0x00000000),
    (0x1E, 0x00000000),
    (0x1F, 0x00000000),
    (0x20, 0x1FFF1770),
    (0x21, 0x1FFF1770),
    (0x22, 0x0E1004B0),
    (0x23, 0x0E1004B0),
    (0x24, 0x1C2012C0),
    (0x25, 0x1C2012C0),
    (0x26, 0x09600000),
    (0x27, 0x09600000),
    (0x28, 0x1FFF1770),
    (0x29, 0x1FFF1770),
    (0x2A, 0x0E1004B0),
    (0x2B, 0x0E1004B0),
    (0x2C, 0x1C2012C0),
    (0x2D, 0x1C2012C0),
    (0x2E, 0x09600000),
    (0x2F, 0x09600000),
    (0x120, 0xF1F2F2F2),
    (0x121, 0x0007F1F1),
]

cfgfile_values = []

# Define a function to write to the tx7332 chip
def write_to_chip(tx7332, register_address, register_value, id):
    print(f"Writing to register 0x{register_address:X}: 0x{register_value:X}")
    tx7332.write_block(register_address, register_value, id)

def read_from_chip(tx7332, register_address, expected_value, id):
    register_value = tx7332.read_register(register_address, id)
    if(expected_value != register_value):
        print(f"Read from register 0x{register_address:X}: 0x{expected_value:X}  0x{register_value:X}")
        return False
    return True

def ustx_write_config(tx7332, id):
    print("Writing Config Registers to USTX Started")
    tx7332.write_block(cfgfile_values, id)
    print("Writing Config Registers to USTX Completed")

def enable_tx(tx7332):
    tx7332.start_trigger()
    # GREEN LED should be on
    
def disable_tx(tx7332):
    tx7332.stop_trigger()
    # GREEN LED should be off

def verify_test_config(tx7332):
    # Check each register value
    for register_address, expected_value in test_config_values:
        register_value = tx7332.read_register(register_address, 0)
        if register_value != expected_value:
            print(f"ERROR Read from register 0x{register_address:X}: 0x{expected_value:X}  0x{register_value:X}")

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Process a .cfg file and write to the tx7332 chip.")

    # Add an argument for the cfg file name
    parser.add_argument("cfg_file", help="Path to the .cfg file")

    # Parse the command-line arguments
    args = parser.parse_args()
    bPassed = True

    # Open and read the .cfg file specified by the user
    
    cfgfile_values.clear()
    with open(args.cfg_file, 'r') as cfg_file:
        for line in cfg_file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                register_address, register_value = parts
                register_address = int(register_address.split('|')[1], 16)
                register_value = int(register_value, 16)
                # Append the register address and value as a tuple to the reg_values list
                cfgfile_values.append((register_address, register_value))



    if bPassed:
        print("PASSED registers match file")
    else:
        print("FAILED check above mismatches")

if __name__ == "__main__":

    # Select communication port
    s = UART('COM24')

    # Simulate initializing the tx7332 object        
    tx7332 = TX7332(s)

    disable_tx(tx7332)
    #write_to_chip(tx7332, 0x20, 0x7017FF1F, 0)

    #verify_test_config(tx7332)

    #disable_tx(tx7332)
    json_data = {
        "TriggerFrequencyHz": 100,
        "TriggerMode": 0,
        "TriggerPulseCount": 0,
        "TriggerPulseWidthUsec": 500
    }
        
    tx7332.set_trigger(json_data)
    r = tx7332.get_trigger()
    print(r)
    main()
    ustx_write_config(tx7332, 0)
    time.sleep(1)
    print("Turn on Trigger")
    enable_tx(tx7332)
    # disable_tx(tx7332)
    # Close serial port
    s.close()