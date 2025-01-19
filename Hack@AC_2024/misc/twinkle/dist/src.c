#include <Adafruit_NeoPixel.h>

#define PIN            6
#define NUMPIXELS      8
#define DELAY_MS       2000
#define TIME_BTWN_PACKET 3000

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);
char channels[] = {'R', 'G', 'B'};
uint8_t data[] = "[some data that contains the flag]";
bool toSend = true;

void clear() {
  for (int i = 0; i < NUMPIXELS; i++) {
    pixels.setPixelColor(i, pixels.Color(0, 0, 0));
  }
  pixels.show();
}

void sendData(char channel, uint8_t* data, int len) {
  //indicate start of packet and Set LED 0 to White
  clear();
  pixels.setPixelColor(0, pixels.Color(255, 255, 255));
  pixels.show();
  delay(DELAY_MS);
  
  // Set the LED 0 to the corresponding channel
  if (channel == 'R') {
    pixels.setPixelColor(0, pixels.Color(255, 0, 0));
  } else if (channel == 'G') {
    pixels.setPixelColor(0, pixels.Color(0, 255, 0));
  } else if (channel == 'B') {
    pixels.setPixelColor(0, pixels.Color(0, 0, 255));
  }
    
  // Send data
  for (int i = 0; i < 7; i++) {
    uint8_t r = channel == 'R' ? (i < len ? data[i] : 0) : random(255);
    uint8_t g = channel == 'G' ? (i < len ? data[i] : 0) : random(255);
    uint8_t b = channel == 'B' ? (i < len ? data[i] : 0) : random(255);
    
    pixels.setPixelColor(i + 1, pixels.Color(r, g, b));
  }
  
  //display
  pixels.show();
}

void setup() {
  // Init Serial
  Serial.begin(115200);

  pixels.begin();
  // Clear strip
  clear();
}

void loop() {
  // wait for serial input before executing following code. once executed, never execute again
  while (!Serial.available());
  String input = Serial.readString();
  if (input != "start") {
    Serial.println("Invalid input");
    return;
  } else if (input == "start" && toSend) {
      Serial.println("Starting");
      // Send data in chunks
      for (int i = 0; i < sizeof(data); i += 7) {
        char channel = channels[random(3)];
        sendData(channel, data + i, min(sizeof(data) - i, 7));
        delay(TIME_BTWN_PACKET);
      }
      clear();
      toSend = false;
      Serial.println("Done");
  }
}