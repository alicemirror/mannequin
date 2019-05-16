/******************************************
 *Website: www.elegoo.com
 * 
 *Time:2017.12.12
 *
 ******************************************/
#define redpin A3 //select the pin for the red LED
#define greenpin 4 // select the pin for the green LED
#define bluepin 5 // select the pin for the  blue LED

int val;
void setup() { pinMode(redpin, OUTPUT); pinMode(bluepin, OUTPUT); pinMode(greenpin, OUTPUT); Serial.begin(9600);
}
void loop()
{
for(val=255; val>0; val--)
{
analogWrite(redpin, val); analogWrite(greenpin, 255-val); analogWrite(bluepin, 128-val); delay(50);
}
for(val=0; val<255; val++)
{
analogWrite(redpin, val); analogWrite(greenpin, 255-val); analogWrite(bluepin, 128-val); delay(50);
}
Serial.println(val, DEC);
}
