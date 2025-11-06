import os
import shutil
import arcpy

# Ścieżki do folderów
folder_shp = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\1863_SHP_2020"
folder_new_shp = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\new_1863_SHP_2020"
gdb_path = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"

# --- NOWE: Tworzenie folderu wyjściowego, jeśli nie istnieje ---
os.makedirs(folder_new_shp, exist_ok=True)
print(f"Folder wyjściowy: {folder_new_shp} (utworzony jeśli nie istniał)")

# Ustawienie środowiska ArcGIS
arcpy.env.workspace = gdb_path
arcpy.env.overwriteOutput = True  # Zezwala na nadpisywanie istniejących warstw

# Krok 1: Kopiowanie plików shapefile z poprawą nazw (kropki → podkreślenia)
print("Krok 1: Kopiowanie i zmiana nazw plików shapefile...")
for file in os.listdir(folder_shp):
    file_path = os.path.join(folder_shp, file)
    
    # Pomijamy pliki blokady i katalogi
    if file.endswith(".sr.lock") or os.path.isdir(file_path):
        continue
    
    # Tylko pliki należące do shapefile (rozszerzenia typowe dla SHP)
    if file.lower().endswith(('.shp', '.shx', '.dbf', '.prj', '.cpg', '.sbn', '.sbx')):
        name, ext = os.path.splitext(file)
        new_name = name.replace(".", "_") + ext
        dest_path = os.path.join(folder_new_shp, new_name)
        
        try:
            shutil.copy(file_path, dest_path)
            print(f"Skopiowano: {file} → {new_name}")
        except Exception as e:
            print(f"Błąd kopiowania {file}: {e}")

# Krok 2: Eksport shapefile do GDB z nową nazwą
print("\nKrok 2: Eksport do geobazy danych...")
for new_file in os.listdir(folder_new_shp):
    if new_file.lower().endswith(".shp"):
        shp_path = os.path.join(folder_new_shp, new_file)
        name_only = os.path.splitext(new_file)[0]
        
        # Bezpieczne wyodrębnienie części po "__" – zakładamy format: coś__nazwa.shp
        if "__" in name_only:
            try:
                suffix = name_only.split("__", 1)[1]  # bierzemy wszystko po pierwszym "__"
                output_feature_class = f"R2020_{suffix}"
                
                print(f"Eksportuję: {new_file} → {output_feature_class}")
                arcpy.conversion.ExportFeatures(
                    in_features=shp_path,
                    out_features=output_feature_class
                )
            except Exception as e:
                print(f"Błąd eksportu {new_file}: {e}")
        else:
            print(f"Pominięto {new_file} – brak '__' w nazwie")

print("\nKONIEC – przetwarzanie zakończone.")