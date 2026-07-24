/*
 * i2c_slave.h
 *
 *  Created on: Mar 4, 2024
 *      Author: gvigelet
 */

#ifndef INC_I2C_SLAVE_H_
#define INC_I2C_SLAVE_H_

#include "main.h"
#include <stdio.h>

enum DeviceState {
  // initial state
  STATE_READY = 0xAA,
  // FW Receive
  STATE_RECEIVING_FW = 0xCC,
  // FW Update Error
  STATE_ERROR = 0xDD,
  // FW Update complete
  STATE_COMPLETED_PACKET = 0x55
};

// Function prototypes for I2C slave operations
void I2C_Slave_Init(uint8_t addr);
void I2C_Slave_ProcessData(uint8_t data);


#endif /* INC_I2C_SLAVE_H_ */
