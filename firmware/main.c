#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"

// Määritellään pinnit
#define POWER_PIN 15
#define ADC_PIN 26
#define ADC_CHANNEL 0 // GP26 on ADC-kanava 0

float calculate_moisture(uint16_t adc);

int main(void)
{
    stdio_init_all();
    gpio_init(POWER_PIN);
    gpio_set_dir(POWER_PIN, GPIO_OUT);
    gpio_put(POWER_PIN, 0); // Varmistetaan, että virta on aluksi pois päältä
    adc_init();
    adc_gpio_init(ADC_PIN);
    adc_select_input(ADC_CHANNEL);

    // Annetaan USB-yhteydelle aikaa aueta ennen tulostelua
    while (!stdio_usb_connected())
    {
        sleep_ms(100);
    }
    printf("DIY Mullan Kosteusmittari (Pico 2W) käynnistetty!\n");

    while (true)
    {
        gpio_put(POWER_PIN, 1);
        sleep_ms(10);
        const float conversion_factor = 3.3f / (1 << 12);
        uint16_t raw_value = adc_read();
        gpio_put(POWER_PIN, 0);
        float moisture = calculate_moisture(raw_value);
        printf("Mullan kosteus (raaka-arvo): %d, Voltit %.2f V, Suhteellinen kosteus %.2f %%\n",
               raw_value, raw_value * conversion_factor, moisture);
        sleep_ms(2000);
    }
    return 0;
}

// Funktio, joka laskee kosteuden regressiokaavan avulla
float regression(float x)
{
    return 0.0000909081f * x * x - 0.244061f * x + 177.237f;
}

// Funktio, joka laskee mullan kosteuden suhteellisina prosentteina ADC-arvon perusteella
float calculate_moisture(uint16_t adc)
{
    // 1342 ADC on mitä realistisesti tarkottaa kuiva multa, ei multa jossa olisi 0g vettä
    const float dry_adc = 1342.0f;
    const float wet_adc = 3400.0f;

    if (adc <= dry_adc)
        return 0.0f;

    if (adc >= wet_adc)
        return 100.0f;

    float moisture = (regression(adc) - regression(dry_adc)) / (regression(wet_adc) - regression(dry_adc)) * 100.0f;

    return moisture;
}
