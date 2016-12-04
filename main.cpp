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
#include <string>
 
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

Serial interLink(P0_2, P0_1); // tx, rx```

uint8_t h = 12;
uint8_t m = 0;
uint8_t s = 0;

uint8_t alarm_h;
uint8_t alarm_m;
uint8_t alarm_s;
bool alarm=false;

void sendNeo(uint8_t r, uint8_t g, uint8_t b) {
    interLink.printf("%02d,%02d,%02d\n",r,g,b);
}

void sendTime() {
    // this runs every second
    
    // Increment the time
    s++;
    if(s>59) {
        m++;
        if(m>59) {
            h++;
            if(h>12) {
                h=1;
            }
            m=0;
        }
        s=0;
    }
    
    // if we have an alarm enabled
    if(alarm) {
        if(alarm_s==s && alarm_m==m && alarm_h==h) {
            // set the alarm off!
            alarm=false;
            interLink.printf("|\n"); // Send an alarm
        }
    }
    
    //-----This block maps the time onto the neopixel
    uint8_t temp_s = (s/5)%60;
    if(temp_s==0) temp_s=12;
    uint8_t temp_m = (m/5)%60;
    if(temp_m==0) temp_m=12;
    uint8_t temp_h = h%13;
    if(h>12) temp_h++;
    //-----------------------------------------
    sendNeo(temp_h,temp_s,temp_m);

}

void periodicCallback() {
    sendTime();
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
        uint8_t identifier = *params->data;
        if(identifier==1) {
            h = *(params->data+1);
            m = *(params->data+2);
            s = *(params->data+3);
        }
        
        else if (identifier==2) {
            alarm_h = *(params->data+1);
            alarm_m = *(params->data+2);
            alarm_s = *(params->data+3);
            alarm = 1;
        }
        
        else if (identifier==3) {
            interLink.printf("!\n");
        }
        
        else if (identifier==4) {
            interLink.printf("*\n");
        }
        
        else {
            int n;
            interLink.printf(";");
            for(n=0; n<(bytesRead); n++) {
                interLink.printf("%c", *(params->data+n));
                }
            interLink.printf("\n");
        }
        
    }
}

 
int main(void)
{
    interLink.baud(115200);
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
    ble.accumulateAdvertisingPayload(GapAdvertisingData::COMPLETE_LOCAL_NAME,
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