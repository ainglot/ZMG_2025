import arcpy

## WFS - siatka NMT: https://mapy.geoportal.gov.pl/wss/service/PZGIK/NumerycznyModelTerenuEVRF2007/WFS/Skorowidze

# Ustawienie geobazy roboczej
arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"
# Nazwa warstwy (feature class)
WarstwaLinie = "DrogaNaRysy_PL92"

# Lista na współrzędne (jeśli chcesz je później wykorzystać)
ListCoorLinie = []
cursor = arcpy.da.SearchCursor(WarstwaLinie, ["SHAPE@"])

i = 0
for row in cursor:
    geom = row[0]  # obiekt geometryczny linii
    # print(f"--- Obiekt {i} ---")
    
    ListCoorOb = []
    # Iteracja po częściach (część = pojedyncza linia lub segment multipart)
    for part in geom:
        # print("  Część obiektu:")
        
        # Iteracja po wierzchołkach danej części
        for pnt in part:
            if pnt:  # niektóre części mogą mieć None
                # print(f"    Wierzchołek: X={pnt.X}, Y={pnt.Y}")
                ListCoorOb.append((pnt.X+100, pnt.Y+100))  # zapis do listy
    # print(ListCoorOb)
    ListCoorLinie.append(ListCoorOb)
    i += 1

print(len(ListCoorLinie[0]))


##### RASTRY
Folder_rastry = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\NMT_TATRY"
arcpy.env.workspace = Folder_rastry

# Get and print a list of GRIDs from the workspace
rasters = arcpy.ListRasters("*", "GRID")
for raster in rasters:
    print(raster)



print("KONIEC")