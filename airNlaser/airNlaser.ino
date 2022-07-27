const int buttonPin = 2;
const int laserPin_L = 3;
const int laserPin_R = 4;
const int valvePin = 5;
const int regulatorPin = 6;
const int PWM_Freq = 1000;
const int PWM_Step = 12;
bool buttonState = false;
int isPushed = 0;

void setup() {
  Serial.begin(9600);
  pinMode(buttonPin, INPUT);
  pinMode(laserPin_L, OUTPUT);
  pinMode(laserPin_R, OUTPUT);
  pinMode(valvePin, OUTPUT);
  pinMode(regulatorPin, OUTPUT);
  analogWrite(regulatorPin, 300);
  digitalWrite(valvePin, 0);
}

void loop() {
  isPushed = digitalRead(buttonPin);
  if (Serial.available() > 0) {
    char cmd = Serial.read();
    if (cmd == 'z') {
      buttonState = true;
      Serial.println("Laser pointer turned on.");
    } else if (cmd == 'x') {
      buttonState = false;
      Serial.println("Laser pointer turned off.");
    } else if (cmd == 'y') {
      digitalWrite(valvePin, 1);
      Serial.println("Valve opened");   
    } else if (cmd == 'n') {
      digitalWrite(valvePin, 0);
      Serial.println("Valve closed");      
    } else if (cmd == 'f') {
      digitalWrite(valvePin, 1);
      delay(3000);
      digitalWrite(valvePin, 0);
      Serial.println("Fire");    
    }else if (cmd == 'p') {
      configPressure();
    }
  }
  if (isPushed) {
    buttonState = !buttonState;
    delay(400);
  }
  if (buttonState == true) {
    digitalWrite(laserPin_L, 1);
    digitalWrite(laserPin_R, 1);
  } 
  if (buttonState == false) {
    digitalWrite(laserPin_L, 0);
    digitalWrite(laserPin_R, 0);
  }
}

void configPressure() {
  int pressure = parseData();
  analogWrite(regulatorPin, pressure);
}

int parseData() {
  String num = "";
  char c;
   for (int i = 0; i < 4; i++){
      while (true) {
        if (Serial.available()) {
          c = Serial.read();
          break;
        }
      }
      num += c;   
   }
   return num.toInt();
}