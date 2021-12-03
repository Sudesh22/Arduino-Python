#include <EduIntro.h>

DHT11 dht11(D7);  // Sensor is connected to pin 'D7'

int C;   // Variable for storing temperature in Degree Celsius
int H;   // Variable for storing Humidity

void setup()
{
  Serial.begin(9600); // Initiating Serial Communication at 9600 baudrate
}

void loop()
{
  dht11.update();

  C = dht11.readCelsius();      // Getting the temperature readings in °C
  H = dht11.readHumidity();     // Getting the humidity index

  // Printing data that can be analysed by Python
  Serial.print("H: ");
  Serial.print(H);
  Serial.print("\tC: ");
  Serial.println(C);

  delay(1000);                // Delaying Readings by a sec
}
