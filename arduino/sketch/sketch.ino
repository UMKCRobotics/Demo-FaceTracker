#include <Servo.h>

int servo1pin = 6;
int servo2pin = 9;
static int start_pos = 85;
Servo servo1;
Servo servo2;
String command;
int change1;
int change2;
int position1;
int position2;

void setup() {
  // put your setup code here, to run once:
  pinMode(servo1pin,OUTPUT);
  pinMode(servo2pin,OUTPUT);
  change1 = 0;
  change2 = 0;
  position1 = start_pos;
  position2 = start_pos-4;
  servo1.attach(servo1pin);
  servo2.attach(servo2pin);
  Serial.begin(115200);
  //Serial.begin(57600);
  Serial.write('1');
  servo1.write(position1);
  servo2.write(position2);
}

void loop() {

  //int reading = analogRead(sensorIn); 
  //Serial.println(reading);
  //servoMove(reading);
  command = "";
  if(Serial.available()){
    while (Serial.available() > 0)
    {
      char readIn = (char)Serial.read();
      if (readIn == '\n') {
        break;
      }
      command += readIn;
      delay(1);
    }
    Serial.println(command);

    if (command.length() == 4) {
      servoCommander1(command[0],command[1]);
      servoCommander2(command[2],command[3]);
    }
  }

  servoControl1(position1+change1);
  servoControl2(position2+change2);
  change1 = 0;
  change2 = 0;
}

void servoCommander1(char action, char amount)
{
  if (action == 'n') {
    change1 = 0;
  }
  else if (action == 'p') {
    change1 = ((int)amount-48);
  }
  else if (action == 'm') {
    change1 = ((int)amount-48)*-1;
  }
  if (abs(change1) > 10) {
    change1 = 0;
  }
}

void servoCommander2(char action, char amount)
{
  if (action == 'n') {
    change2 = 0;
  }
  else if (action == 'p') {
    change2 = ((int)amount-48);
  }
  else if (action == 'm') {
    change2 = ((int)amount-48)*-1;
  }
  if (abs(change2) > 10) {
    change2 = 0;
  }
}


void servoControl1(int pos)
{
  int conmin = 10;
  int conmax = 180;
  pos = constrain(pos,conmin,conmax);
  position1 = pos;
  servo1.write(pos);
}

void servoControl2(int pos)
{
  int conmin = 0;
  int conmax = 170;
  pos = constrain(pos,conmin,conmax);
  position2 = pos;
  servo2.write(pos);
}
