#include <Adafruit_GFX.h>
#include <Adafruit_NeoMatrix.h>
#include <Adafruit_NeoPixel.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

#define PIN 3

// MATRIX DECLARATION:
// Parameter 1 = width of NeoPixel matrix
// Parameter 2 = height of matrix
// Parameter 3 = pin number (most are valid)
// Parameter 4 = matrix layout flags, add together as needed:
//   NEO_MATRIX_TOP, NEO_MATRIX_BOTTOM, NEO_MATRIX_LEFT, NEO_MATRIX_RIGHT:
//     Position of the FIRST LED in the matrix; pick two, e.g.
//     NEO_MATRIX_TOP + NEO_MATRIX_LEFT for the top-left corner.
//   NEO_MATRIX_ROWS, NEO_MATRIX_COLUMNS: LEDs are arranged in horizontal
//     rows or in vertical columns, respectively; pick one or the other.
//   NEO_MATRIX_PROGRESSIVE, NEO_MATRIX_ZIGZAG: all rows/columns proceed
//     in the same order, or alternate lines reverse direction; pick one.
//   See example below for these values in action.
// Parameter 5 = pixel type flags, add together as needed:
//   NEO_KHZ800  800 KHz bitstream (most NeoPixel products w/WS2812 LEDs)
//   NEO_KHZ400  400 KHz (classic 'v1' (not v2) FLORA pixels, WS2811 drivers)
//   NEO_GRB     Pixels are wired for GRB bitstream (most NeoPixel products)
//   NEO_RGB     Pixels are wired for RGB bitstream (v1 FLORA pixels, not v2)

const char* ssid     = "";
const char* password = "";
ESP8266WebServer server(80);

Adafruit_NeoMatrix matrix = Adafruit_NeoMatrix(32, 8, 2, 1, PIN,
  NEO_MATRIX_TOP    + NEO_MATRIX_LEFT +
  NEO_MATRIX_COLUMNS + NEO_MATRIX_ZIGZAG,
  NEO_GRB            + NEO_KHZ800);

String display = ""; 
String post = "";
int x = matrix.width();
int c = 0;
int refresh = 35;

void setup() {
  Serial.begin(115200);
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
    Serial.println(display);
//    matrix_scroll(25);
  }

  display = "Connected! " + WiFi.localIP().toString();
//  matrix_scroll(27);
  Serial.println(display);
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
 post = server.arg("plain");
 server.send(200, "text/plain", "Body received\n" + post + "\n");
 Serial.println(post);
// matrix_scroll();
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
