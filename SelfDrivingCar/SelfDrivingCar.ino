int BIN2 = 4;
int PWMB = 5;
int PWMA = 6;
int AIN1 = 7;
int BIN1 = 9;
int AIN2 = 10;
float distance;
#include <Wire.h>
#define uchar unsigned char
uchar t;
//void send_data(short a1,short b1,short c1,short d1,short e1,short f1);
uchar data[16];
int thresh = 93;
int loSpeed = 0;
int medSpeed = 50;
int hiSpeed = 70;
int defSpeed = 90;
unsigned long start;
int state = 0;
int lastState = 0;
String light = "";
String sign = "";
String turn = "";

void setup() {
  // put your setup code here, to run once:


pinMode (BIN2, OUTPUT);
pinMode (PWMB, OUTPUT);
pinMode (PWMA, OUTPUT);
pinMode (AIN1, OUTPUT);
pinMode (BIN1, OUTPUT);
pinMode (AIN2, OUTPUT);

digitalWrite (BIN2,LOW);
digitalWrite (PWMB,LOW);
digitalWrite (PWMA,LOW);
digitalWrite (AIN1,LOW);
digitalWrite (BIN1,LOW);
digitalWrite (AIN2,LOW);

delay(200);
digitalWrite(AIN1, HIGH);
digitalWrite(BIN1, HIGH);

Serial.begin(9600);
Wire.begin();
 t = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())  // if data available in serial port
    { 
    light = Serial.readStringUntil(','); // read data until newline
    sign = Serial.readStringUntil('.');
    turn = Serial.readStringUntil('\n');

    if(light == "yellow"){
      goSlow();
    }
    else if(light == "red"){
      stahp();
    }
    if(sign == "Yes"){
      stahp();
      delay(3000);
      goForward();
    }
    if(turn == "right"){
      driveRight();
      delay(1500);
    }
    else if(turn == "left"){
    driveLeft();
    delay(1500);
}
    else{
      goForward(); 
    }
}
}

void goForward(int duration){
  analogWrite (PWMB, defSpeed);
  analogWrite (PWMA, defSpeed);
  digitalWrite(AIN1, HIGH);
  digitalWrite(BIN1, HIGH);
}
void goBackwards(int duration){
  digitalWrite(AIN2, HIGH);
  digitalWrite(BIN2, HIGH);
}
void goRight(int duration){
  digitalWrite(BIN1, HIGH);
  delay(duration);
  digitalWrite(BIN1, LOW);
  //delay(duration);
}
void goLeft(int duration){
  digitalWrite(AIN1, HIGH);
  delay(duration);
  digitalWrite(AIN1, LOW);
  //delay(duration);
}
void driveForward(){
analogWrite (PWMB, defSpeed);
analogWrite (PWMA, defSpeed);
}
void stahp(){
  digitalWrite(AIN1, LOW);
  digitalWrite(BIN1, LOW);
  digitalWrite(AIN2, LOW);
  digitalWrite(BIN2, LOW);
}
void driveRight(){
analogWrite (PWMB, defSpeed);
analogWrite (PWMA, hiSpeed);
}
void driveLeft(){
analogWrite (PWMB, hiSpeed);
analogWrite (PWMA, defSpeed);
}
void driveRightMed(){
analogWrite (PWMB, defSpeed);
analogWrite (PWMA, medSpeed);
}
void driveLeftMed(){
analogWrite (PWMB, medSpeed);
analogWrite (PWMA, defSpeed);
}
void driveRightHi(){
analogWrite (PWMB, defSpeed);
analogWrite (PWMA, loSpeed);
}
void driveLeftHi(){
analogWrite (PWMB, loSpeed);
analogWrite (PWMA, defSpeed);
}
void goSlow(){
  analogWrite(PWMA, medspeed);
  analogWrite(PWMB, medspeed);
}

