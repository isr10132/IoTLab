#include <SoftwareSerial.h>
#include "DHT.h"
#define DHTPIN 2
#define DHTTYPE DHT22

SoftwareSerial AT(8, 9);
DHT dht(DHTPIN, DHTTYPE);
char val;

void setup() {
  Serial.begin(9600);
  Serial.println("AT is ready!");
  dht.begin();

  // set the buadrate of module
  // if NB-IoT 4553 set to 115200
  AT.begin(9600);
  delay(3000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);

  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(f);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.print(hif);
  Serial.println(F("°F"));

//  String dataCommand = getDataCommand(h, t);
  String humidityRingCommand = getHumidityRingCommand(h, 1);
  
  sendATCommand("AT", 100);
  sendATCommand("AT+CSQ", 100); // test connection
  sendATCommand("AT+QSCLK=0", 100);
  sendATCommand("AT+QBAND=1,8", 100);
  sendATCommand("AT+CFUN=1", 100);
  sendATCommand("AT+CGSN=1", 100);
  sendATCommand("AT+CIMI", 100);
  sendATCommand("AT+CFUN=1", 100);
  sendATCommand("AT+CGATT=0", 3000);
  sendATCommand("AT+CGDCONT=1,\"IPV4V6\"", 2000);
  sendATCommand("AT+CGATT=1", 4000);
  sendATCommand("AT+QICFG=\"dataformat\",1,1", 2000);
  sendATCommand("AT+QIOPEN=1,0,\"TCP\",140.114.78.132,16631,0,0,0", 4000);
  sendATCommand(humidityRingCommand.c_str(), 4000);

  String ring_state = sendATCommand("AT+QIRD=0,500", 4000);
  Serial.println("ring_state:"+ring_state);
}
/*
String getDataCommand(float humidity, float temperature) {
  char buf[64];
  String output = "AT+QISENDEX=0,9,";
  char tmp[2];
  dtostrf(humidity, 2, 1, buf);
  for(int i=0; i<4; i++) {
    sprintf(tmp, "%X", buf[i]);
    output += tmp;
  }
  output += "2C";
  dtostrf(temperature, 2, 1, buf);
  for(int i=0; i<4; i++) {
    sprintf(tmp, "%X", buf[i]);
    output += tmp;
  }
  return output;
}
*/
String getHumidityRingCommand(float humidity, int ring_state) {
  char buf[64];
  String output = "AT+QISENDEX=0,6,";
  char tmp[2];
  dtostrf(humidity, 2, 1, buf);
  for(int i=0; i<4; i++) {
    sprintf(tmp, "%X", buf[i]);
    output += tmp;
  }
  output += "2C";
  String hexString = String(ring_state+30);
  output += hexString;
  return output;
}

String sendATCommand(const char *toSend, unsigned long milliseconds) {
  String result;
//  Serial.print("Sending: ");
//  Serial.println(toSend);
  AT.println(toSend);
  unsigned long startTime = millis();
//  Serial.print("Received: ");
  while(millis() - startTime < milliseconds) {
    if (AT.available()) {
      char c = AT.read();
      Serial.write(c);
      result += c;
    }
  }
  Serial.println();
  return result;
}

void loop() {
  // If receive message from IDE, send it to module
  if (Serial.available()) {
    val = Serial.read();
    Serial.flush();
    AT.print(val);
  }

  // If receive message from module, display on IDE
  if (AT.available()) {
    val = AT.read();
    Serial.print(val);
    Serial.flush();
  }
}
