import arcpy
import numpy as np

arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG"

RasterIn = "77225_1309395_6.221.26.11.3.asc"

def distance_from_center(shape, pixel_size=1.0):
    """
    shape: (rows, cols) - rozmiar rastra
    pixel_size: rozdzielczość przestrzenna (np. 10 m/piksel)
    """
    rows, cols = shape

    # Indeksy wierszy i kolumn
    y_idx, x_idx = np.indices((rows, cols))

    # Środek rastra (może być niecałkowity przy parzystych wymiarach)
    cy = (rows - 1) / 2.0
    cx = (cols - 1) / 2.0

    # Różnice w jednostkach pikseli
    dy = (y_idx - cy) * pixel_size
    dx = (x_idx - cx) * pixel_size

    # Odległość euklidesowa od środka
    dist = np.hypot(dx, dy)  # to samo co np.sqrt(dx**2 + dy**2)

    return dist

arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(2177) #przypisanie układu współrzędnych do rastra wyjściowego
R = arcpy.Raster(RasterIn)
LewyDolnyPunkt = arcpy.Point(R.extent.XMin, R.extent.YMin) #przechowanie współrzędnych do lokalizacji rastra wyjściowego
print(R.extent.XMin, R.extent.YMin)
RozdzielczoscPrzestrzenna = R.meanCellWidth #rozdzielczość przestrzenna rastra
print(RozdzielczoscPrzestrzenna)
NoData = 0 #wartość NoData - w tym rastrze minimalna wartość jest większa niż 0, można tak wykonać


# Przykład użycia:
dist_mat = distance_from_center((5, 5), pixel_size=RozdzielczoscPrzestrzenna)
print(dist_mat)
