int x; 
void setup() { 
	Serial.begin(9600);
  
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(3,OUTPUT);
  pinMode(11,OUTPUT);
  pinMode(10,OUTPUT);
  pinMode(2,OUTPUT);
  



	//Serial.setTimeout(1); 
} 
void loop() { 
	

	while (!Serial.available());
  x = 0;
	x = Serial.read();

  
  digitalWrite(2, LOW);
  digitalWrite(3, HIGH);
 
  analogWrite(10, x);
  analogWrite(11, x);
  Ssrial.close()
} 
