#define K1 4
#define K2 5
#define K3 6
#define K4 7
#define K5 8
#define K6 9
#define K7 10
#define K8 11

void setup(){
  pinMode(K8,OUTPUT);
  pinMode(K7,OUTPUT);
  pinMode(K6,OUTPUT);
  pinMode(K5,OUTPUT);
  pinMode(K4,OUTPUT);
  pinMode(K3,OUTPUT);
  pinMode(K2,OUTPUT);
  pinMode(K1,OUTPUT);

  digitalWrite(K8, HIGH);
  digitalWrite(K7, HIGH);
  digitalWrite(K6, HIGH);
  digitalWrite(K5, HIGH);
  digitalWrite(K4, HIGH);
  digitalWrite(K3, HIGH);
  digitalWrite(K2, HIGH);
  digitalWrite(K1, HIGH);

  Serial.begin(9600);
}
void loop(){
  String inputString="";
  int count=0;
  while(Serial.available()){
    inputString=Serial.readStringUntil('\n');

  }
  
  // Serial.print(inputString);
  if(inputString == "P1"){
    resetPort();
    // Wire A : K1 OPEN, K2 OPEN 
    // Wire B: K5 OPEN, K6 OPEN
    //do nothing because default
    
  }
  if (inputString == "P2"){
    resetPort();
    // Wire A : K1 OPEN, K2 CLOSE 
    // Wire B: K5 OPEN, K6 CLOSE
      digitalWrite(K2, LOW);
      digitalWrite(K5, LOW);
  }
  if (inputString == "P3"){
    resetPort();
    // Wire A : K1 CLOSE, K3 OPEN 
    // Wire B: K5 CLOSE, K7 OPEN
    digitalWrite(K1, LOW);
    digitalWrite(K4, LOW);
  }
  if (inputString == "P4"){
    resetPort();
    // Wire A : K1 CLOSE, K3 CLOSE 
    // Wire B: K5 CLOSE, K6 CLOSE
    digitalWrite(K1, LOW);
    digitalWrite(K4, LOW);
    digitalWrite(K3, LOW);
    digitalWrite(K6, LOW);
  }
  if (inputString== "CC"){
    // K7 CLOSE, K8 CLOSE
    digitalWrite(K7, LOW);
    digitalWrite(K8, LOW);
  }
  if (inputString== "BO"){
    // K7 OPEN, K8 OPEN
    digitalWrite(K7, HIGH);
    digitalWrite(K8, HIGH);
  }

}
void resetPort(){
  digitalWrite(K6, HIGH);
  digitalWrite(K5, HIGH);
  digitalWrite(K4, HIGH);
  digitalWrite(K3, HIGH);
  digitalWrite(K2, HIGH);
  digitalWrite(K1, HIGH);
}