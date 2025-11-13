import arcpy
import os

# --- Ustawienia ---
gdb_path = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"
txt_path = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\data.txt"
output_fc_name = "Punkty_z_txt" #54.528821794446145, 18.557495816016086

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
            # Z jest opcjonalne – ignorujemy je w 2D
            ListCoor.append([x, y])
        except ValueError as e:
            print(f"Błąd w linii {line_num}: {line} -> {e}")

if not ListCoor:
    raise ValueError("Nie wczytano żadnych poprawnych współrzędnych.")

# --- Utwórz nową warstwę punktową ---
spatial_reference = arcpy.Describe("R2014_OT_ADMS_P").spatialReference  # przejmij układ z istniejącej warstwy
# Alternatywnie: arcpy.SpatialReference(4326) dla WGS84, jeśli dane są w stopniach

arcpy.management.CreateFeatureclass(
    out_path=gdb_path,
    out_name=output_fc_name,
    geometry_type="POINT",
    template="",  # opcjonalnie: przejmij schemat (pola, domeny)
    spatial_reference=spatial_reference
)

# --- Wstaw punkty ---
with arcpy.da.InsertCursor(output_fc_name, ["SHAPE@X", "SHAPE@Y"]) as cursor:
    for coor in ListCoor:
        cursor.insertRow(coor)

print(f"Utworzono warstwę: {output_fc_name} z {len(ListCoor)} punktami.")