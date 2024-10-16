#include <Servo.h>

Servo myservo;

int pos = 90;


void setup() 
{
  myservo.attach(13);
}


void loop() 
{
  myservo.write(pos);
  delay(1000);
  myservo.write(40);
  delay(1000);
}