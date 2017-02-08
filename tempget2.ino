//Analog Temperature Sensor
int analogPin = A0; // Analog Temperature Sensor pin A0 to pin A0

// variables will change:
int Astate = 0; // variable for reading status of A0
//int temp2 = Astate * 12300;
//float temp2 = 1/temp;

void setup() 
{
Serial.begin(9600); // initialize serial communications at 9600 bps
}


void loop()
{
Astate = analogRead(analogPin); // read Analog Temperature Sensor A0 value (set point)
Serial.println(Astate);//print the value of temp


delay(1000); // controls speed of Analog Temperature Sensor and Serial Monitor display rate
}
