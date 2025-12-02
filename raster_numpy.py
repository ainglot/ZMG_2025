import arcpy
import numpy as np

arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG"

RasterIn = "77225_1309395_6.221.26.11.3.asc"

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2177) #przypisanie układu współrzędnych do rastra wyjściowego
R = arcpy.Raster(RasterIn)
LewyDolnyPunkt = arcpy.Point(R.extent.XMin, R.extent.YMin) #przechowanie współrzędnych do lokalizacji rastra wyjściowego
print(R.extent.XMin, R.extent.YMin)
RozdzielczoscPrzestrzenna = R.meanCellWidth #rozdzielczość przestrzenna rastra
print(RozdzielczoscPrzestrzenna)
NoData = np.nan #wartość NoData - w tym rastrze minimalna wartość jest większa niż 0, można tak wykonać

R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = NoData)

min_flat = np.nanargmin(R_array)
max_flat = np.nanargmax(R_array)

min_row, min_col = np.unravel_index(min_flat, R_array.shape)
max_row, max_col = np.unravel_index(max_flat, R_array.shape)

min_val = float(R_array[min_row, min_col])
max_val = float(R_array[max_row, max_col])

ext = R.extent
cell_w = R.meanCellWidth
cell_h = R.meanCellHeight

# X lewy, Y górny z geometrii rastra
x_min = ext.XMin
y_max = ext.YMax

# MIN
min_x = x_min + (min_col + 0.5) * cell_w
min_y = y_max - (min_row + 0.5) * cell_h

# MAX
max_x = x_min + (max_col + 0.5) * cell_w
max_y = y_max - (max_row + 0.5) * cell_h


rows, cols = R_array.shape

out_name = "PunktMinMax.shp"

# Tworzymy pustą klasę obiektów POINT
arcpy.management.CreateFeatureclass(
    out_path=arcpy.env.workspace,
    out_name=out_name,
    geometry_type="POINT",
    spatial_reference=2177
)

# Dodajemy pola na typ punktu i wartość rastra
arcpy.management.AddField(out_name, "PT_TYPE", "TEXT", field_length=10)
arcpy.management.AddField(out_name, "VALUE", "DOUBLE")

# Wstawiamy dwa punkty
with arcpy.da.InsertCursor(out_name, ["SHAPE@X", "SHAPE@Y", "PT_TYPE", "VALUE"]) as cur:
    # MIN
    # p_min = arcpy.Point(min_x, min_y)
    cur.insertRow([min_x, min_y, "MIN", min_val])

    # MAX
    # p_max = arcpy.Point(max_x, max_y)
    cur.insertRow([max_x, max_y, "MAX", max_val])




# print(R_array)

# print("Liczba wierszy:", rows)
# print("Liczba kolumn:", cols)


# R_array[100:200, 100:300] += 10 # W lewym gónym rógó rastra "wycinamy" prostokąt

# outR = arcpy.NumPyArrayToRaster(R_array, LewyDolnyPunkt, RozdzielczoscPrzestrzenna, value_to_nodata = NoData)
# # # zapisać nowy raster trzeba podać - dane (R_array), współrzędne lewego dolnego naroża, rozdzielczość przestrzenną i jaką wartość przyjmuje NoData
# outR.save("NowyRaster02.tif")


print("KONIEC")


# ###########################
# NowaWarstwa = "LewtDolnyPunkt.shp"
# arcpy.management.CreateFeatureclass(arcpy.env.workspace, NowaWarstwa, "POINT", 
#                                     "", "DISABLED", "DISABLED", 
#                                     2177)

# cursor = arcpy.da.InsertCursor(NowaWarstwa, ["SHAPE@X", "SHAPE@Y"])
# # for coor in ListCoor:
# cursor.insertRow([R.extent.XMin, R.extent.YMin])

# del cursor
# ###################################