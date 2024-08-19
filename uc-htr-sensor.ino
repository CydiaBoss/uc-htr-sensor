// I2C Library
#include <Wire.h>

// Address of HT Sensor
short ht_adr = 40;
short read_delay = 1000;

// Pin of Resistor Sensor
int resistor_pin = A0;

// Reference Resistor
float ref_resistor = 1.0;
char resistor_mult = 'k';
float ref_volt = 5.0;
bool resist_stat = true;

// Data Storage
double resistor = -9999;
float rh = -9999;
float temp = -9999;

void setup(){
    // Setup I2C connection
    Wire.begin();
    // Begin Serial connection to computer at 9600 baud
    Serial.begin(9600);
    Serial.setTimeout(1);
    // Setup Message
    Serial.println("\nRunning");
}

void loop(){
    // Check for user input
    while (Serial.available() > 0) {
        switch (char(Serial.read())) {
            // Update Reference Resistor 
            case 'r': {
                ref_resistor = Serial.parseFloat();
                resistor_mult = Serial.read();
                Serial.println("ok (r" + String(ref_resistor) + resistor_mult + ")");
                break;
            }
            // Update Reference Voltage 
            case 'v': {
                ref_volt = Serial.parseFloat();
                Serial.println("ok (v" + String(ref_volt) + ")");
                break;
            }
            // Update Period (ms) 
            case 'p': {
                read_delay = Serial.parseInt();
                Serial.println("ok (p" + String(read_delay) + ")");
                break;
            }
            // Toggle Resistor Reading
            case 't': {
                resist_stat = !resist_stat;
                Serial.println("ok (t" + String(resist_stat) + ")");
                break;
            }
        }
        // Clear buffer
        Serial.flush();
    }
    // Take one reading
    updateMeasurements();
    // Print
    Serial.print(String(resistor_mult) + "Ω:");
    Serial.print(resistor);
    Serial.print(",");
    Serial.print("%RH:");
    Serial.print(rh);
    Serial.print(",");
    Serial.print("°C:");
    Serial.println(temp);
    // Period Delay
    delay(read_delay); 
}

void updateMeasurements(){
    // Read Resistor
    resistor = -1.0;
    if (resist_stat) {
        resistor = ref_volt * (analogRead(resistor_pin) / 1023.0);
        resistor = resistor * ref_resistor / (ref_volt - resistor);
    }
    // Temp Data 
    uint8_t data[4] = {0};
    // Read Raw Data
    Wire.requestFrom(ht_adr, 4);
    for(int i = 0; i < 4; i++) {
      data[i] = Wire.read();
    }
    // Convert RH to percent
    rh = (float)((((data[0] & 0x3F) << 8) + data[1]) / 16384.0) * 100.0; 
    // Convert Temp
    temp = (float)((unsigned((data[2] * 64)) + unsigned((data[3] >> 2))) / 16384.0) * 165.0 - 40.0;  
}