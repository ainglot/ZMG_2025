import arcpy
from collections import defaultdict
import matplotlib.pyplot as plt

# === 1. Ustawienie środowiska i wyszukiwanie warstw ===
arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"
featureclasses = arcpy.ListFeatureClasses()

PT2014_list = []
PT2020_list = []

for fc in featureclasses:
    if "R2014" in fc and "OT_PT" in fc:
        print("2014 - ", fc)
        PT2014_list.append(fc)
    elif "R2020" in fc and "OT_PT" in fc:
        print("2020 - ", fc)
        PT2020_list.append(fc)

print(PT2014_list)
print(PT2020_list)

# === 2. Scalanie warstw ===
PT2014 = "PT_2014"
PT2020 = "PT_2020"

arcpy.management.Merge(PT2014_list, PT2014)
arcpy.management.Merge(PT2020_list, PT2020)

# === 3. Przecięcie przestrzenne ===
inter_2014_2020 = "PT_2014_2020"
arcpy.analysis.Intersect([PT2014, PT2020], inter_2014_2020)

# === 4. Analiza zmian pokrycia (X_KOD) + przygotowanie danych do wykresu ===
area_pary = defaultdict(float)
area_all = 0.0
area_change = 0.0
change_count = 0

with arcpy.da.SearchCursor(inter_2014_2020, ["X_KOD", "X_KOD_1", "Shape_Area"]) as cursor:
    for row in cursor:
        kod_2014, kod_2020, area = row
        area_all += area
        if kod_2014 != kod_2020:
            change_count += 1
            area_change += area
            para = f"{kod_2014}-{kod_2020}"
            area_pary[para] += area

# === 5. Obliczenia procentowe ===
proc_bez_zmian = ((area_all - area_change) / area_all) * 100
proc_zmian = (area_change / area_all) * 100

print(f"Liczba zmian: {change_count}")
print(f"Bez zmian: {proc_bez_zmian:.2f}% | Ze zmianą: {proc_zmian:.2f}%")

# === 6. Przygotowanie danych do wykresu (top N + reszta) ===
area_pary_sort = sorted(area_pary.items(), key=lambda x: x[1], reverse=True)

top_n = 5
new_list = []
area_inne = 0.0
i = 0

for para, area in area_pary_sort:
    procent = (area / area_change) * 100
    if i < top_n:
        new_list.append([para, procent])
    else:
        area_inne += procent
    i += 1

if area_inne > 0:
    new_list.append(["reszta", area_inne])

print("\nTop zmiany (procentowo):")
for item in new_list:
    print(f"{item[0]:<15}: {item[1]:.2f}%")

# === 7. Wykres kołowy ===
wartosci = [x[1] for x in new_list]
etykiety = [x[0] for x in new_list]

plt.figure(figsize=(10, 8))
plt.pie(wartosci, labels=etykiety, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 10})
plt.title(f'Zmiany pokrycia terenu 2014 → 2020\n(top {top_n} typów zmian + reszta)', fontsize=14)
plt.axis('equal')
plt.tight_layout()
plt.show()