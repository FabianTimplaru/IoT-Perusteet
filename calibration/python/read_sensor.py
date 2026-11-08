import serial
import csv
from datetime import datetime
from pathlib import Path

PORT = "COM5"
BAUD_RATE = 115200

# Luodaan mittauksille oma CSV-tiedosto
filename = Path(__file__).resolve().parent.parent / "data" / f"kalibrointi_{datetime.now():%Y%m%d_%H%M%S}.csv"

water_g = 0.0
measurement = 0

with serial.Serial(PORT, BAUD_RATE, timeout=2) as pico:
    with open(filename, "w", newline="", encoding="utf-8") as file:

        writer = csv.writer(file, delimiter=";")
        writer.writerow(["mittaus", "vesi_g", "adc", "jannite_v", "aika"])

        print("MULLANKOSTEUSANTURIN KALIBROINTI")
        print("Enter = mittaa | w = veden määrä | q = lopeta")

        while True:
            command = input(f"\nVesi: {water_g:g} g | Komento: ").strip().lower()

            if command == "q":
                break

            elif command == "w":
                try:
                    new_water = float(
                        input("Lisätty vesi yhteensä (g): ").replace(",", ".")
                    )

                    if new_water < 0:
                        print("Veden määrä ei voi olla negatiivinen.")
                        continue

                    water_g = new_water
                    print(f"Veden määrä päivitetty: {water_g:g} g")

                except ValueError:
                    print("Virheellinen veden määrä.")

            elif command == "":
                pico.write(b"\n")

                response = pico.readline().decode(errors="replace").strip()

                if response.isdigit():
                    adc = int(response)
                    voltage = adc * 3.3 / 4096
                    measurement += 1

                    timestamp = datetime.now().isoformat(timespec="seconds")

                    writer.writerow([measurement, water_g, adc, f"{voltage:.2f}", timestamp])

                    print(f"Mittaus {measurement}: ADC = {adc} | Jännite = {voltage:.2f} V | Vesi = {water_g:g} g")
                    file.flush()
                else:
                    print("Mittaus epäonnistui. Yritä uudelleen.")

            else:
                print("Tuntematon komento.")

print(f"\nMittaukset tallennettu tiedostoon: {filename}")
