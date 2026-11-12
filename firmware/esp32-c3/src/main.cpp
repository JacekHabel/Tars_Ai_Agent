
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <U8g2lib.h>

#define SDA_PIN 8
#define SCL_PIN 9

#define BME280_ADDR_1 0x76
#define BME280_ADDR_2 0x77

// SSD1306 128x64 OLED using hardware I2C
U8G2_SSD1306_128X64_NONAME_F_HW_I2C
    u8g2(U8G2_R0, U8X8_PIN_NONE);

Adafruit_BME280 bme;

bool sensorInitialized = false;

void setup() {
    Serial.begin(115200);
    delay(1000);

    // Initialize I2C
    Wire.begin(SDA_PIN, SCL_PIN);

    // Initialize OLED
    u8g2.begin();
    u8g2.setFont(u8g2_font_6x12_tf);

    u8g2.clearBuffer();
    u8g2.drawStr(0, 15, "BME280 Weather");
    u8g2.drawStr(0, 32, "Initializing...");
    u8g2.sendBuffer();

    Serial.println("ESP32-C3 BME280 Monitor");
    Serial.println("-----------------------");

    // Try address 0x76 first, then 0x77
    sensorInitialized = bme.begin(BME280_ADDR_1, &Wire);

    if (!sensorInitialized) {
        sensorInitialized = bme.begin(BME280_ADDR_2, &Wire);
    }

    if (!sensorInitialized) {
        Serial.println("ERROR: BME280 not detected!");

        u8g2.clearBuffer();
        u8g2.drawStr(0, 15, "BME280 ERROR!");
        u8g2.drawStr(0, 32, "Check wiring");
        u8g2.drawStr(0, 48, "Check I2C address");
        u8g2.sendBuffer();

        while (true) {
            delay(1000);
        }
    }

    // Configure sensor sampling
    bme.setSampling(
        Adafruit_BME280::MODE_NORMAL,
        Adafruit_BME280::SAMPLING_X2,   // Temperature
        Adafruit_BME280::SAMPLING_X16,  // Pressure
        Adafruit_BME280::SAMPLING_X1,   // Humidity
        Adafruit_BME280::FILTER_X16,
        Adafruit_BME280::STANDBY_MS_500
    );

    Serial.println("BME280 initialized successfully.");
    Serial.println();
}

void loop() {
    // Read sensor values
    float temperature = bme.readTemperature();
    float humidity = bme.readHumidity();
    float pressure = bme.readPressure() / 100.0F;

    // Print values to Serial Monitor
    Serial.print("Temperature: ");
    Serial.print(temperature, 2);
    Serial.println(" C");

    Serial.print("Humidity: ");
    Serial.print(humidity, 2);
    Serial.println(" % RH");

    Serial.print("Pressure: ");
    Serial.print(pressure, 2);
    Serial.println(" hPa");

    Serial.println("-----------------------");

    // Update OLED
    char buffer[32];

    u8g2.clearBuffer();

    // Header
    u8g2.setFont(u8g2_font_6x12_tf);
    u8g2.drawStr(0, 12, "BME280 Weather");

    // Temperature
    u8g2.setFont(u8g2_font_helvB12_tf);
    snprintf(buffer, sizeof(buffer), "%.1f C", temperature);
    u8g2.drawStr(0, 30, buffer);

    // Humidity
    u8g2.setFont(u8g2_font_6x12_tf);
    snprintf(buffer, sizeof(buffer), "Humidity: %.1f %%", humidity);
    u8g2.drawStr(0, 44, buffer);

    // Pressure
    snprintf(buffer, sizeof(buffer), "Pressure: %.1f hPa", pressure);
    u8g2.drawStr(0, 59, buffer);

    u8g2.sendBuffer();

    delay(2000);
}