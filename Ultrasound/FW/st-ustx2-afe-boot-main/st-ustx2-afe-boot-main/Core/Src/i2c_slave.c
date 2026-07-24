#include "i2c_slave.h"
#include <stdio.h>
#include <string.h>

#define RXBUFFERSIZE 256
#define DEBUG_COMMS

extern I2C_HandleTypeDef hi2c1;

#define I2C_DEVICE hi2c1

__IO uint32_t uwTransferRequested;

uint8_t ram[RXBUFFERSIZE];
static uint8_t offset; //
uint32_t count = 0;
static uint8_t first=1;// first byte --> new offset

void I2C_Slave_Init(uint8_t addr) {
    memset(ram, 0, RXBUFFERSIZE);
    uwTransferRequested = 1;

    if(addr == 0x00 || addr > 0x3F) {
        I2C_DEVICE.Init.OwnAddress1  = 0x32 << 1;  // default to 0x32
    } else {
        I2C_DEVICE.Init.OwnAddress1  = addr << 1;
    }

    if (HAL_I2C_Init(&I2C_DEVICE) != HAL_OK) {
        // Handle the error if initialization fails
        Error_Handler();
    }

    HAL_I2C_EnableListen_IT(&I2C_DEVICE);

    printf("I2C Slave Started\r\n");
}

void I2C_Slave_Run() {
    // Implement any necessary functionality here
}

void HAL_I2C_AddrCallback(I2C_HandleTypeDef *I2cHandle, uint8_t TransferDirection, uint16_t AddrMatchCode) {
    // Address match callback implementation
    // You can add code here to handle address match events
	if(TransferDirection == I2C_DIRECTION_TRANSMIT)  // if the master wants to transmit the data
	{
	    if( first ) {
	      HAL_I2C_Slave_Seq_Receive_IT(I2cHandle, &offset, 1, I2C_NEXT_FRAME);
	    } else {
	      HAL_I2C_Slave_Seq_Receive_IT(I2cHandle, &ram[offset], 1, I2C_NEXT_FRAME);
	    }
	}
	 else {
		// master wants to receive data
		HAL_I2C_Slave_Seq_Transmit_IT(I2cHandle, &ram[offset], 1, I2C_NEXT_FRAME);

	}
}

void HAL_I2C_SlaveTxCpltCallback(I2C_HandleTypeDef *I2cHandle) {
    // Transmission complete callback implementation
	offset++;
	HAL_I2C_Slave_Seq_Transmit_IT(I2cHandle, &ram[offset], 1, I2C_NEXT_FRAME);
}

void HAL_I2C_SlaveRxCpltCallback(I2C_HandleTypeDef *I2cHandle) {
	  if(first) {
	    first = 0;
	  } else {
	    offset++;
	  }
	  HAL_I2C_Slave_Seq_Receive_IT(I2cHandle, &ram[offset], 1, I2C_NEXT_FRAME);
}

void HAL_I2C_ListenCpltCallback(I2C_HandleTypeDef *I2cHandle) {
	// Listen complete callback implementation
	first = 1;
	HAL_I2C_EnableListen_IT(I2cHandle); // slave is ready again
}

void HAL_I2C_ErrorCallback(I2C_HandleTypeDef *I2cHandle) {
    // Error callback implementation
    uint32_t errorcode = HAL_I2C_GetError(I2cHandle);
	if( HAL_I2C_GetError(I2cHandle)==HAL_I2C_ERROR_AF ) {
		offset--; // transaction terminated by master
	} else {
	    printf("HAL_I2C_ErrorCallback UNHANDLED ERR: 0x%08lX \r\n", errorcode);

	}
}
