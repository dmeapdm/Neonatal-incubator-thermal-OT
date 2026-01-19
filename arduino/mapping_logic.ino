#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

void setup(void) {
    Serial.begin(9600); // inicializa el puerto de comunicacion
    sensors.begin();    // inicializa los 6 sensores
    Serial.print("Sensores encontrados ");
    Serial.println(sensors.getDeviceCount()); // imprime la cantidad de sensores encontrados=6
} // <- cerramos setup correctamente

void loop() {
    sensors.requestTemperatures(); // pide las lecturas de los 6 sensores

    for (int i = 0; i < sensors.getDeviceCount(); i++) {
        float temp = sensors.getTempCByIndex(i);
        Serial.print(temp);
        if (i < sensors.getDeviceCount() - 1) {
            Serial.print(","); // separa con coma
        }
    }
    Serial.println(); // salto de línea al final de la línea
    delay(1000); // Esperar 1 segundo entre lecturas
}
