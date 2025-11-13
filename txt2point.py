import arcpy
import os
from collections import defaultdict

# --- Ustawienia ---
gdb_path = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"
txt_path = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\data.txt"
output_fc_name = "Punkty_z_txt_v3" #54.528821794446145, 18.557495816016086
Centr = [471329.7, 740641.8]

arcpy.env.workspace = gdb_path
# arcpy.env.overwriteOutput = True

# --- Sprawdź, czy plik istnieje ---
if not os.path.exists(txt_path):
    raise FileNotFoundError(f"Nie znaleziono pliku: {txt_path}")

# --- Czytaj współrzędne z pliku ---
ListCoor = []
with open(txt_path, 'r') as f:
    for line_num, line in enumerate(f, 1):
        line = line.strip()
        if not line:  # pomiń puste linie
            continue
        try:
            parts = line.split()
            if len(parts) < 2:
                print(f"Pominięto linię {line_num}: za mało wartości -> {line}")
                continue
            x = float(parts[0])
            y = float(parts[1])
            z = float(parts[2])
            # Z jest opcjonalne – ignorujemy je w 2D
            ListCoor.append([x, y, z])
        except ValueError as e:
            print(f"Błąd w linii {line_num}: {line} -> {e}")

if not ListCoor:
    raise ValueError("Nie wczytano żadnych poprawnych współrzędnych.")

z_values = [row[2] for row in ListCoor]

z_min = min(z_values)
z_max = max(z_values)
print(z_min, z_max)
# --- Oblicz średnie X i Y ---
if ListCoor:
    sum_x = sum(coord[0] for coord in ListCoor)
    sum_y = sum(coord[1] for coord in ListCoor)
    sum_z = sum(coord[2] for coord in ListCoor)
    n = len(ListCoor)

    sr_x = sum_x / n
    sr_y = sum_y / n
    sr_z = sum_z / n

    print(f"Średnia X: {sr_x:.3f}")
    print(f"Średnia Y: {sr_y:.3f}")
    print(f"Średnia Z: {sr_z:.3f}")
    print(f"Punkt środkowy: ({sr_x:.3f}, {sr_y:.3f}, {sr_z:.3f})")
else:
    print("Brak punktów – nie można obliczyć średniej.")

# --- Grupowanie po klasach Z (co 2) ---
classes = defaultdict(list)  # klucz: klasa Z, wartość: lista [x, y]

for x, y, z in ListCoor:
    if z < 0:
        # opcjonalnie: przesuń ujemne Z do 0 lub pomiń
        continue  # lub: z = max(0, z)
    
    class_id = int(z // 2) * 2  # np. 0, 2, 4, ...
    classes[class_id].append([x, y])

# --- Oblicz średnie dla każdej klasy ---
print("Średnie X i Y dla klas Z:\n")
print(f"{'Klasa Z':<10} {'Średnia X':<12} {'Średnia Y':<12} {'Liczba pkt'}")
print("-" * 50)

for class_z in sorted(classes.keys()):
    points = classes[class_z]
    n = len(points)
    if n == 0:
        continue
    
    avg_x = sum(p[0] for p in points) / n
    avg_y = sum(p[1] for p in points) / n
    
    range_str = f"[{class_z}, {class_z + 2})"
    print(f"{range_str:<10} {avg_x:12.3f} {avg_y:12.3f} {n:8}")

# --- Opcjonalnie: dodaj punkty średnie do warstwy ---
NowaWarstwa = "Srednie_Klasy_Zv3"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, NowaWarstwa, "POINT", spatial_reference=arcpy.Describe("R2014_OT_ADMS_P").spatialReference)

with arcpy.da.InsertCursor(NowaWarstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
    for class_z in sorted(classes.keys()):
        points = classes[class_z]
        n = len(points)
        if n == 0: continue
        avg_x = sum(p[0] for p in points) / n
        avg_y = sum(p[1] for p in points) / n
        new_coor = [avg_x-sr_x+Centr[0], avg_y-sr_y+Centr[1]]
        cursor.insertRow(new_coor)


# # --- Utwórz nową warstwę punktową ---
# spatial_reference = arcpy.Describe("R2014_OT_ADMS_P").spatialReference  # przejmij układ z istniejącej warstwy
# # Alternatywnie: arcpy.SpatialReference(4326) dla WGS84, jeśli dane są w stopniach

# arcpy.management.CreateFeatureclass(
#     out_path=gdb_path,
#     out_name=output_fc_name,
#     geometry_type="POINT",
#     template="",  # opcjonalnie: przejmij schemat (pola, domeny)
#     spatial_reference=spatial_reference
# )

# # --- Wstaw punkty ---
# with arcpy.da.InsertCursor(output_fc_name, ["SHAPE@X", "SHAPE@Y"]) as cursor:
#     for coor in ListCoor:
#         new_coor = [coor[0]-sr_x+Centr[0], coor[1]-sr_y+Centr[1]]
#         cursor.insertRow(new_coor)

# print(f"Utworzono warstwę: {output_fc_name} z {len(ListCoor)} punktami.")