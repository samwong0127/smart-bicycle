int relay1 = 2;//pin 2 connect to relay 1
int relay2 = 3;//pin 3 connect to relay2

void setup() {
 Serial.begin(9600);
 pinMode(relay1, OUTPUT);
 pinMode(relay2, OUTPUT);
}

void loop() {
  if (Serial.available() > 0)
  {
    char state = Serial.read();
    
 if (state == '1')//if siganl is high
    {
    digitalWrite(relay1,HIGH);
    digitalWrite(relay2,LOW);
    Serial.println("Motor speed up."); 
 }
 else if(state == '0')
    {
    digitalWrite(relay1,LOW);
    digitalWrite(relay2,LOW);
    Serial.println("Stop Motor.");
  }
 }
}
