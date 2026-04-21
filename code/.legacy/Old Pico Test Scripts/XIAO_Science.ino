// XIAO Seeduino Firmware - Continuous Stream

#include <Wire.h>
#include <SparkFun_Soil_Moisture_Sensor.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// ------------------------------
// Soil Moisture (I2C)
// ------------------------------
SparkFunSoilMoistureSensor soil;

// ------------------------------
// DS18B20
// ------------------------------
#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature ds18b20(&oneWire);

// ------------------------------
unsigned long lastPrint = 0;
const unsigned long printInterval = 200;   // 5 Hz

// ------------------------------
void setup()
{
  Serial.begin(115200);
  Wire.begin();
  soil.begin();
  ds18b20.begin();
}

// ------------------------------
void loop()
{
  if (millis() - lastPrint > printInterval)
  {
    lastPrint = millis();

    uint16_t moisture = soil.readMoistureValue();

    ds18b20.requestTemperatures();
    float tempC = ds18b20.getTempCByIndex(0);  // will be -127 if not found

    Serial.print(moisture);
    Serial.print(",");
    Serial.println(tempC);
  }
}