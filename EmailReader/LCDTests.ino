// include the library code:
#include <LiquidCrystal.h>

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 12, en = 11, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);
String clearLine = "                ";
String message;
boolean alternate = false;
String substring1;
String substring2;
String substring3;

void setup() {
  Serial.begin(9600);
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("Waiting for");
  lcd.setCursor(0, 1);
  lcd.print("message!");
  lcd.setCursor(0, 0);
}


void getSubstrings(String messages){
  String str1 = "";
  String str2 = "";
  String str3 = "";
  int sz = messages.length();
  int state = 0;
  
  if(messages.indexOf('/') >= 0){
    for(int i = 0; i < sz; i++){
      if(messages.charAt(i) == '/'){
        state += 1;
      } else{
        switch(state){
          case 0:
            str1 += messages.charAt(i);
            break;
          case 1:
            str2 += messages.charAt(i);
            break;
          case 2:
            str3 += messages.charAt(i);
            break;
        }
      }
    }
  }

  substring1 = str1;
  substring2 = str2;
  substring3 = str3;

  if(str3.length() == 0){
    alternate = false;
  } else{
    alternate = true;
  }
}

void alternateScreen(){
  Serial.println("Alternating!");
  delay(100);
  lcd.setCursor(0, 0);
  lcd.print(substring1);
  delay(100);
  lcd.setCursor(0, 1);
  lcd.print(substring2);
  delay(4000);
  clearScreen();
  lcd.print(substring3);
  delay(4000);
}

String parseMessage(String message){
  int lastSpace;
  int sz = message.length();
  for(int i = 0; i < sz; i++){
    if(message.charAt(i) == ' ' && i <= 16){
      lastSpace = i;
    }
  }

  String str1 = "";
  String str2 = "";
  for(int i = 0; i < sz; i++){
    if(i < lastSpace){
      str1 += message.charAt(i);
    } else if(i > lastSpace){
      str2 += message.charAt(i);
    }
  }

  if(str2.length() > 16){
    return str1 + "/" + parseMessage(str2);
  } else{
    return str1 + "/" + str2;
  }
}

void clearScreen(){
  lcd.setCursor(0, 0);
  lcd.print(clearLine);
  lcd.setCursor(0, 1);
  lcd.print(clearLine);
  lcd.setCursor(0, 0);              
}

void loop() {
  while(Serial.available()){
    clearScreen();
    message = Serial.readString();
    Serial.println("Original: " + message);
    //message.remove(message.length()- 1, 2);
    message.trim();
    message.replace(',', ' ');
    if(message.length() > 16){
      message = parseMessage(message);
      Serial.println("Parsed Message: " + message);
      getSubstrings(message);
      Serial.println(alternate);
      if(!alternate){
        lcd.print(substring1);
        lcd.setCursor(0, 1);
        lcd.print(substring2);
      }
    } else{
      lcd.print(message);
    }
  }

  if(alternate){
    alternateScreen();
  }
}
