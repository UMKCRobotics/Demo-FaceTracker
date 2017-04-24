#include <Servo.h>

#define SERVO1_PIN 6
#define SERVO2_PIN 9

static int start_pos = 85;

Servo servo1;
Servo servo2;

// servo positions
int position1;
int position2;
// delay time
const int delayTime = 2;
// input parsing
const int maxValues = 2;
String command; // general command
String values[maxValues]; // stores values for command
String response; // response returned to main program




void setup() {
  // put your setup code here, to run once:
  pinMode(SERVO1_PIN,OUTPUT);
  pinMode(SERVO2_PIN,OUTPUT);

  position1 = start_pos;
  position2 = start_pos-4;

  servo1.attach(SERVO1_PIN);
  servo2.attach(SERVO2_PIN);
  
  Serial.begin(115200);
  Serial.write('1');
  
  servo1.write(position1);
  servo2.write(position2);
}

void loop() {

  // if something in serial, parse it
  if(Serial.available()){

    int addTo = 0; // 0 for command, 1 for value

    while (Serial.available() > 0)
    {
      char readIn = (char)Serial.read();
      if (readIn == '\n') {
        break;
      }
      else if (readIn == '|') {
        addTo += 1;
        continue;
      }
      // add to command if no | reached yet
      if (addTo == 0) {
        command += readIn;
      }
      // add to proper value in array
      else if (addTo <= maxValues) {
        values[addTo-1] += readIn;
      }
      // if values exceed max, then stop listening to prevent problems
      else {
        break;
      }
    }
    //clear anything remaining in serial
    while (Serial.available() > 0) {
      Serial.read();
    }
    response = interpretCommand();
    Serial.println(response); //sends response with \n at the end
    // empty out command and value strings
    command = "";
    for (int i = 0; i < maxValues; i++) {
      values[i] = "";
    }
  }
  // delay a bit
  delay(delayTime);
  
}

String interpretCommand() {
  String responseString = "n";  // string to be sent to main program
  String returnString = "";     // string received from a subfunction
  // determine what to do:
  if (command == "m") {
    // check if values have appropriate lengths
    if (values[0].length() != 2 || values[1].length() != 2)
      return responseString;
    // if valid, do servo movements
    else {
      responseString = "1";
      responseString += incrementServo1(getServoChange(values[0][0],values[0][1]));
      responseString += incrementServo2(getServoChange(values[1][0],values[1][1]));
    }
  }
  
  responseString += returnString;
  return responseString;
}


int getServoChange(char action, char amount) {
  int change;
  if (action == 'n') {
    change = 0;
  }
  else if (action == 'p') {
    change = ((int)amount-48);
  }
  else if (action == 'm') {
    change = ((int)amount-48)*-1;
  }
  if (abs(change) > 10) {
    change = 0;
  }
  return change;
}

int incrementServo1(int change) {
  int conmin = 10;
  int conmax = 180;
  position1 = constrain(position1+change,conmin,conmax);
  servo1.write(position1);
  return position1;
}

int incrementServo2(int change) {
  int conmin = 0;
  int conmax = 170;
  position2 = constrain(position2+change,conmin,conmax);
  servo2.write(position2);
  return position2;
}
