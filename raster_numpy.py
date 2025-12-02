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
NoData = 0 #wartość NoData - w tym rastrze minimalna wartość jest większa niż 0, można tak wykonać

R_array = arcpy.RasterToNumPyArray(R, nodata_to_value = NoData)

rows, cols = R_array.shape

print(R_array)

print("Liczba wierszy:", rows)
print("Liczba kolumn:", cols)


R_array[100:200, 100:300] += 10 # W lewym gónym rógó rastra "wycinamy" prostokąt

outR = arcpy.NumPyArrayToRaster(R_array, LewyDolnyPunkt, RozdzielczoscPrzestrzenna, value_to_nodata = NoData)
# # zapisać nowy raster trzeba podać - dane (R_array), współrzędne lewego dolnego naroża, rozdzielczość przestrzenną i jaką wartość przyjmuje NoData
outR.save("NowyRaster02.tif")


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