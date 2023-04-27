#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h> //устанавливаем
#include <Adafruit_SSD1306.h> //устанавливаем
#include <OneWire.h> //устанавливаем
#include <DallasTemperature.h> //устанавливаем

#define OLED_RESET 7
#define ONE_WIRE_BUS 8

OneWire oneWire(ONE_WIRE_BUS);
Adafruit_SSD1306 display(OLED_RESET); 
DallasTemperature sensors(&oneWire);


int PCdata[5]; //массив полученных чисел
String msg = "";
int index;
bool start = false;

void setup() {
    Serial.begin(9600); //
    
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C); 
    display.clearDisplay(); 
    display.setTextSize(2);
    display.setTextColor(WHITE);
    
    display.setCursor(0, 0);  //заставка
    display.print ("DEBIK");
    display.setCursor(0, 16); 
    display.print ("DEVELOPMENT");
    display.display();
  
    index = 0;
}

void loop() {
  if (Serial.available() > 0) {  //наполняем массив полученными числами
    int data = Serial.parseInt();
    PCdata[index] = data;
    index ++;
    if (index == 5) 
      {
        while(Serial.available()) Serial.read();  //цикл освобождения serial
        for (int i=0; i<=4; i++) msg = msg + String(PCdata[i]) + " "; //сообщение для проверки
        index = 0;
        Serial.println(msg);
        msg = "";
        Serial.flush(); 

        display.clearDisplay(); //инфа cpu
        display.setCursor(0, 0);
        display.print("C_TEMP " + String(PCdata[1]) + "C");
        display.setCursor(0, 16);
        display.print("C_LOAD " + String(PCdata[0]) + "%");
        display.display();
        delay(2000);

        display.clearDisplay(); //инфа gpu
        display.setCursor(0, 0);
        display.print("G_TEMP " + String(PCdata[3]) + "C");
        display.setCursor(0, 16);
        display.print("G_LOAD " + String(PCdata[4]) + "%");
        display.display();
        delay(2000);

        sensors.requestTemperatures(); //показания с датчика температуры
        display.clearDisplay(); //инфа gpu
        display.setCursor(0, 0);
        display.print("S_TEMP " + String(int(sensors.getTempCByIndex(0))) + "C");
        display.setCursor(0, 16);
        display.print("R_LOAD " + String(PCdata[2]) + "%");
        display.display();
        delay(2000);
      }
    delay(500);
  }
}
