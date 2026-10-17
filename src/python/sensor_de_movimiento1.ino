int LED =5;
int PIR =4;


void setup()
{
  pinMode(LED, OUTPUT);
  pinMode(PIR, INPUT);
}

void loop()
{
  int value = digitalRead(PIR);
  if (value == 1) {
  digitalWrite(LED, HIGH);
    }
 else
   {
   digitalWrite(LED, LOW);
}
    delay(10);
    }