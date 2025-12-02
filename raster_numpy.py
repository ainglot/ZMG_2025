import arcpy
import numpy as np

# ==========================
# 1. USTAWIENIA ŚRODOWISKA
# ==========================
arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG"

# Nazwa rastra wejściowego (musi być w workspace)
RasterIn = "77225_1309395_6.221.26.11.3.asc"

# Układ współrzędnych dla wyników (EPSG 2177)
sr_2177 = arcpy.SpatialReference(2177)
arcpy.env.outputCoordinateSystem = sr_2177


# ==========================
# 2. WCZYTANIE RASTRA I PODSTAWOWE PARAMETRY
# ==========================
R = arcpy.Raster(RasterIn)

# Lewy dolny punkt rastra (przydatny przy tworzeniu nowego rastra z NumPy)
LewyDolnyPunkt = arcpy.Point(R.extent.XMin, R.extent.YMin)
print("Lewy dolny narożnik rastra:", R.extent.XMin, R.extent.YMin)

# Rozdzielczość przestrzenna
RozdzielczoscPrzestrzenna = R.meanCellWidth
print("Rozdzielczość przestrzenna:", RozdzielczoscPrzestrzenna)

# Wartość NoData w tablicy NumPy
# (tu przyjmujemy np.nan, bo minimalna wartość rastra > 0)
NoData = np.nan


# ==========================
# 3. RASTER → TABLICA NUMPY
# ==========================
R_array = arcpy.RasterToNumPyArray(
    R,
    nodata_to_value=NoData
)

# Wymiary tablicy (wiersze, kolumny)
rows, cols = R_array.shape
# print("Liczba wierszy:", rows)
# print("Liczba kolumn:", cols)


# ==========================
# 4. SZUKANIE MINIMUM I MAKSIMUM W TABLICY
# ==========================
# nanargmin / nanargmax ignorują wartości np.nan
min_flat = np.nanargmin(R_array)
max_flat = np.nanargmax(R_array)

# Zamiana indeksu spłaszczonego na (wiersz, kolumna)
min_row, min_col = np.unravel_index(min_flat, R_array.shape)
max_row, max_col = np.unravel_index(max_flat, R_array.shape)

# Wartości rastra w punktach min / max
min_val = float(R_array[min_row, min_col])
max_val = float(R_array[max_row, max_col])


# ==========================
# 5. ZAMIANA (WIERSZ, KOLUMNA) → WSPÓŁRZĘDNE XY
# ==========================
ext = R.extent
cell_w = R.meanCellWidth
cell_h = R.meanCellHeight

# XMin i YMax z rastra
x_min = ext.XMin
y_max = ext.YMax

# Środek piksela = XMin + (col + 0.5)*cell_w, YMax - (row + 0.5)*cell_h

# MIN
min_x = x_min + (min_col + 0.5) * cell_w
min_y = y_max - (min_row + 0.5) * cell_h

# MAX
max_x = x_min + (max_col + 0.5) * cell_w
max_y = y_max - (max_row + 0.5) * cell_h


# ==========================
# 6. TWORZENIE WARSTWY PUNKTOWEJ I DODANIE MIN / MAX
# ==========================
out_name = "PunktMinMax.shp"

# Tworzymy pustą klasę obiektów typu POINT
arcpy.management.CreateFeatureclass(
    out_path=arcpy.env.workspace,
    out_name=out_name,
    geometry_type="POINT",
    spatial_reference=sr_2177
)

# Dodajemy pola na typ punktu i wartość rastra
arcpy.management.AddField(out_name, "PT_TYPE", "TEXT", field_length=10)
arcpy.management.AddField(out_name, "VALUE", "DOUBLE")

# Wstawiamy dwa punkty: MIN i MAX
with arcpy.da.InsertCursor(out_name, ["SHAPE@X", "SHAPE@Y", "PT_TYPE", "VALUE"]) as cur:
    # MIN
    cur.insertRow([min_x, min_y, "MIN", min_val])

    # MAX
    cur.insertRow([max_x, max_y, "MAX", max_val])


# ==========================
# 7. KOD OPCJONALNY (PRZYKŁAD MODYFIKACJI RASTRA)
# ==========================
# Przykład: modyfikacja fragmentu rastra i zapis do nowego pliku
#
# R_array[100:200, 100:300] += 10  # prostokąt w lewym górnym rogu
#
# outR = arcpy.NumPyArrayToRaster(
#     R_array,
#     LewyDolnyPunkt,
#     RozdzielczoscPrzestrzenna,
#     value_to_nodata=NoData
# )
# outR.save("NowyRaster02.tif")


print("KONIEC")


# ==========================
# 8. KOD ARCHIWALNY / POMOCNICZY (ZACHOWANY JAKO REFERENCJA)
# ==========================
# Przykład tworzenia punktu w lewym dolnym narożniku rastra:
#
# NowaWarstwa = "LewyDolnyPunkt.shp"
# arcpy.management.CreateFeatureclass(
#     arcpy.env.workspace,
#     NowaWarstwa,
#     "POINT",
#     "",
#     "DISABLED",
#     "DISABLED",
#     sr_2177
# )
#
# with arcpy.da.InsertCursor(NowaWarstwa, ["SHAPE@X", "SHAPE@Y"]) as cursor:
#     cursor.insertRow([R.extent.XMin, R.extent.YMin])
