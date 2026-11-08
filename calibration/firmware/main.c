
#include <stdio.h>
#include "pico/stdlib.h"
#include "hardware/adc.h"

#define POWER_PIN 15
#define ADC_PIN 26

int main(void)
{
    stdio_init_all();

    gpio_init(POWER_PIN);
    gpio_set_dir(POWER_PIN, GPIO_OUT);
    gpio_put(POWER_PIN, 0);

    adc_init();
    adc_gpio_init(ADC_PIN);
    adc_select_input(0);

    while (!stdio_usb_connected())
        sleep_ms(100);

    while (true)
    {
        // Odotetaan Enter-painallusta
        if (getchar() != '\n')
            continue;

        // Kytketään anturi päälle
        gpio_put(POWER_PIN, 1);
        sleep_ms(10);

        // Luetaan mittaus ja katkaistaan virta
        uint16_t value = adc_read();
        gpio_put(POWER_PIN, 0);

        // Lähetetään arvo tietokoneelle
        printf("%u\n", value);
    }
}
