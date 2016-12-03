/* mbed Microcontroller Library
 * Copyright (c) 2006-2013 ARM Limited
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
#include "mbed.h"
#include "ble/BLE.h"
 
#include "ble/services/UARTService.h"
 
#define NEED_CONSOLE_OUTPUT 0 /* Set this if you need debug messages on the console;
                               * it will have an impact on code-size and power consumption. */
 
#if NEED_CONSOLE_OUTPUT
#define DEBUG(...) { printf(__VA_ARGS__); }
#else
#define DEBUG(...) /* nothing */
#endif /* #if NEED_CONSOLE_OUTPUT */
 
BLEDevice  ble;
DigitalOut led1(LED1);
 
UARTService *uartServicePtr;

Serial interLink(USBTX, USBRX); // tx, rx```


void sendTime(uint8_t h, uint8_t m, uint8_t s) {
    uint8_t r = 0;
    uint8_t g = 0;
    uint8_t b = 0;
    interLink.printf("%02d,%02d,%02d\n",r,g,b);
}
 
void disconnectionCallback(const Gap::DisconnectionCallbackParams_t *params)
{
    DEBUG("Disconnected!\n\r");
    DEBUG("Restarting the advertising process\n\r");
    ble.startAdvertising();
}
 
void onDataWritten(const GattWriteCallbackParams *params)
{
    if ((uartServicePtr != NULL) && (params->handle == uartServicePtr->getTXCharacteristicHandle())) {
        uint16_t bytesRead = params->len;
        DEBUG("received %u bytes\n\r", bytesRead);
        ble.updateCharacteristicValue(uartServicePtr->getRXCharacteristicHandle(), params->data, bytesRead);
        uint8_t h = *params->data;
        uint8_t m = *(params->data+1);
        uint8_t s = *(params->data+2);
        sendTime(h,m,s);
        
    }
}
 
void periodicCallback(void)
{
    led1 = !led1;
}
 
int main(void)
{
    led1 = 1;
    Ticker ticker;
    ticker.attach(periodicCallback, 1);
 
    DEBUG("Initialising the nRF51822\n\r");
    ble.init();
    ble.onDisconnection(disconnectionCallback);
    ble.onDataWritten(onDataWritten);
 
    /* setup advertising */
    ble.accumulateAdvertisingPayload(GapAdvertisingData::BREDR_NOT_SUPPORTED);
    ble.setAdvertisingType(GapAdvertisingParams::ADV_CONNECTABLE_UNDIRECTED);
    ble.accumulateAdvertisingPayload(GapAdvertisingData::SHORTENED_LOCAL_NAME,
                                     (const uint8_t *)"JoshWatch", sizeof("JoshWatch") - 1);
    ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LIST_128BIT_SERVICE_IDS,
                                     (const uint8_t *)UARTServiceUUID_reversed, sizeof(UARTServiceUUID_reversed));
 
    ble.setAdvertisingInterval(500); /* 1000ms; in multiples of 0.625ms. */
    ble.startAdvertising();
 
    UARTService uartService(ble);
    uartServicePtr = &uartService;
 
    while (true) {
        ble.waitForEvent();
    }
}