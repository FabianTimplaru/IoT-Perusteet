
import csv
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

# ASETUKSET
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PLOTS_DIR = BASE_DIR / "plots"

GROUP_SIZE = 5
POLYNOMIAL_DEGREE = 2

PLOTS_DIR.mkdir(exist_ok=True)

# 1. LUETAAN UUSIN MITTAUSTIEDOSTO

files = list(DATA_DIR.glob("kalibrointi_*.csv"))

if not files:
    raise SystemExit("Kalibrointitiedostoa ei löytynyt!")

filename = max(files, key=lambda f: f.stat().st_mtime)

print(f"Luetaan tiedosto: {filename.name}")

water = []
adc = []

with open(filename, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file, delimiter=";")

    for row in reader:
        if not row["adc"] or not row["vesi_g"]:
            continue

        adc.append(float(row["adc"].replace(",", ".")))
        water.append(float(row["vesi_g"].replace(",", ".")))

adc = np.array(adc)
water = np.array(water)

print(f"Mittauksia yhteensä: {len(adc)}")

# 2. TARKISTETAAN RYHMITTELY

if len(adc) == 0 or len(adc) % GROUP_SIZE != 0:
    raise SystemExit(
        f"Mittauksia täytyy olla viidellä jaollinen! "
        f"Nyt: {len(adc)}"
    )

adc_groups = adc.reshape(-1, GROUP_SIZE)
water_groups = water.reshape(-1, GROUP_SIZE)

# Varmistetaan, ettei samaan ryhmään kuulu eri vesimääriä
for i, group in enumerate(water_groups, start=1):
    if not np.allclose(group, group[0]):
        raise SystemExit(
            f"Ryhmässä {i} on eri vesimääriä: {group}. "
            "Tarkista CSV-tiedoston rivit."
        )

# 3. LASKETAAN KESKIARVOT

adc_avg = np.mean(adc_groups, axis=1)
water_avg = np.mean(water_groups, axis=1)

print(f"Keskiarvopisteitä: {len(adc_avg)}")

# Tallennetaan keskiarvot myös CSV-tiedostoon
average_file = DATA_DIR / f"keskiarvot_{filename.stem}.csv"

with open(average_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file, delimiter=";")
    writer.writerow(
        ["ryhma", "vesi_g", "adc_keskiarvo", "jannite_v"]
    )

    for i, (a, w) in enumerate(zip(adc_avg, water_avg), start=1):
        voltage = a * 3.3 / 4096
        writer.writerow([i, f"{w:.1f}", f"{a:.2f}", f"{voltage:.2f}"])

# 4. KUVAAJA 1 - KAIKKI MITTAUKSET

fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(adc, water, alpha=0.65)

ax.set_title("Kaikki mittauspisteet")
ax.set_xlabel("ADC-arvo")
ax.set_ylabel("Lisätty vesi (g)")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(PLOTS_DIR / "01_kaikki_mittaukset.png", dpi=300)

plt.show()
plt.close(fig)

# 5. KUVAAJA 2 - KESKIARVOT

fig, ax = plt.subplots(figsize=(10, 6))

ax.scatter(adc_avg, water_avg, s=55)

ax.set_title("Viiden mittauksen keskiarvot")
ax.set_xlabel("ADC-keskiarvo")
ax.set_ylabel("Lisätty vesi (g)")
ax.grid(True, alpha=0.3)

fig.tight_layout()
fig.savefig(PLOTS_DIR / "02_keskiarvot.png", dpi=300)

plt.show()
plt.close(fig)

# 6. POLYNOMIREGRESSIO

# ADC on selittävä muuttuja (x)
# Lisätty vesimäärä on ennustettava muuttuja (y)

if len(adc_avg) <= POLYNOMIAL_DEGREE:
    raise SystemExit("Liian vähän pisteitä regressioon!")

coefficients = np.polyfit(
    adc_avg,
    water_avg,
    POLYNOMIAL_DEGREE
)

polynomial = np.poly1d(coefficients)

predictions = polynomial(adc_avg)

# R²-arvon laskenta
ss_res = np.sum((water_avg - predictions) ** 2)
ss_tot = np.sum((water_avg - np.mean(water_avg)) ** 2)

if ss_tot == 0:
    raise SystemExit("Vesimäärissä ei ole vaihtelua!")

r_squared = 1 - ss_res / ss_tot

# Piirretään sovitettu käyrä
x_line = np.linspace(min(adc_avg), max(adc_avg), 500)
y_line = polynomial(x_line)

a, b, c = coefficients

equation = (
    f"Vesi (g) = {a:.6g} × ADC² "
    f"{b:+.6g} × ADC {c:+.6g}"
)

# 7. KUVAAJA 3 - KESKIARVOT JA REGRESSIO

fig, ax = plt.subplots(figsize=(11, 7))

ax.scatter(adc_avg, water_avg, s=55, label="Keskiarvot")
ax.plot(x_line, y_line, label="Polynomiregressio")

ax.set_title("Mullankosteusanturin kalibrointikäyrä")
ax.set_xlabel("ADC-keskiarvo")
ax.set_ylabel("Lisätty vesi (g)")
ax.grid(True, alpha=0.3)
ax.legend()

ax.text(
    0.03,
    0.97,
    f"{equation}\nR² = {r_squared:.4f}",
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(facecolor="white", alpha=0.9, edgecolor="gray")
)

fig.tight_layout()
fig.savefig(PLOTS_DIR / "03_regressio.png", dpi=300)

plt.show()
plt.close(fig)

# 8. TULOSTETAAN TULOKSET

print("\nKALIBROINNIN TULOKSET")
print("-" * 40)
print(f"Mittauksia: {len(adc)}")
print(f"Keskiarvopisteitä: {len(adc_avg)}")
print(f"Regressioaste: {POLYNOMIAL_DEGREE}")
print(f"Yhtälö: {equation}")
print(f"R² = {r_squared:.4f}")
print(f"\nKeskiarvot tallennettu: {average_file}")
print(f"Kuvaajat tallennettu: {PLOTS_DIR}")
