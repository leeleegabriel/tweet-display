#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#define PIN 3

const char* ssid     = "";
const char* password = "";
ESP8266WebServer server(80);

Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(32, 8, 2, 1, PIN,
  NEO_MATRIX_TOP    + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

String display = ""; 
int x = matrix.width();
int c = 0;
int refresh = 35;

void setup() {
//  Serial.begin(115200);
  WiFi.begin(ssid, password);
  matrix.begin();
  matrix.setTextWrap(false);
  matrix.setBrightness(30);
  matrix.setTextColor(matrix.Color(255, 0, 0));
  matrix.fillScreen(0);
  matrix.show();
  
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    display = "Waiting to connect . . . ";
//    Serial.println(display);
    matrix_scroll(25);
  }

  display = "Connected! " + WiFi.localIP().toString();
  matrix_scroll(27);
//  Serial.println(display);
  server.on("/body", handleBody);
  server.begin();
}

void loop() {
  server.handleClient();
}

void handleBody() {
  if (server.hasArg("plain")== false){ //Check if body received
    server.send(200, "text/plain", "Body not received");
    return;
 }
 display = server.arg("plain");
 server.send(200, "text/plain", "Body received\n" + display + "\n");
// Serial.println(display);
 matrix_scroll(300);
}

void matrix_scroll(int c) {
  x = matrix.width();
  while(--x > (c * -12)) { 
    matrix.fillScreen(0);
    matrix.setCursor(x, 0);
    matrix.print(display);
    matrix.show();
    delay(refresh);
  }  
}
