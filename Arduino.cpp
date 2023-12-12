#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

 
#define buzzer 12 
#define led 13 
 
#define x A0 
#define y A1 
#define z A2 
 
/*variables*/
int xsample=0;
int ysample=0;
int zsample=0;
long start;
int buz=0;
 
/*Macros*/
#define samples 50
#define maxVal 20
#define minVal -20 
#define buzTime 5000 
 

 LiquidCrystal_I2C lcd(0x27,16,2);

void setup()
{
lcd.init();
lcd.backlight();
Serial.begin(9600); 
delay(1000);
lcd.print("Sismografo ");
lcd.setCursor(0,1);
lcd.print("Fisica Ondas ");
delay(2000);
lcd.clear();
lcd.print("Calibrando");
lcd.setCursor(0,1);
lcd.print("Espere");
pinMode(buzzer, OUTPUT);
pinMode(led, OUTPUT);
buz=0;
digitalWrite(buzzer, buz);
digitalWrite(led, buz);
for(int i=0;i<samples;i++) 
{
xsample+=analogRead(x);
ysample+=analogRead(y);
zsample+=analogRead(z);
}
 
xsample/=samples; 
ysample/=samples; 
zsample/=samples; 
 
delay(3000);
lcd.clear();
lcd.print("Calibrado");
delay(1000);
lcd.clear();
lcd.print("Dispositivo");
lcd.setCursor(0,1);
lcd.print("Listo");
delay(1000);
lcd.clear();
lcd.print("|X____Y______Z_| ");
}
 
void loop()
{

int value1=analogRead(x); 
int value2=analogRead(y); 
int value3=analogRead(z); 
 
int xValue=xsample-value1; 
int yValue=ysample-value2; 
int zValue=zsample-value3; 
 

lcd.setCursor(0,1);
lcd.print(xValue);
lcd.setCursor(6,1);
lcd.print(yValue);
lcd.setCursor(12,1);
lcd.print(zValue);
delay(100);
 

if(xValue < minVal || xValue > maxVal || yValue < minVal || yValue > maxVal || zValue < minVal || zValue > maxVal)
{
if(buz == 0)
start=millis(); 
buz=1; 
}
 
else if(buz == 1) 
{
lcd.setCursor(0,0);
lcd.print("Alertaaaa ");
if(millis()>= start+buzTime)
buz=0;
}
 
else
{
lcd.clear();
lcd.print("|X____Y______Z_| ");
}
 
digitalWrite(buzzer, buz); 
digitalWrite(led, buz); 
 

Serial.print("x=");
Serial.println(xValue);
Serial.print("y=");
Serial.println(yValue);
Serial.print("z=");
Serial.println(zValue);
Serial.println(" $");

}
