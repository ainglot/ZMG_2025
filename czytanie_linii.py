import arcpy

# Ustawienie geobazy roboczej
arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"

# Nazwa warstwy (feature class)
WarstwaLinie = "R2014_OT_SWRS_L"

# Lista na współrzędne (jeśli chcesz je później wykorzystać)
ListCoorLinie = []

# SearchCursor – odczyt geometrii (SHAPE@) w postaci obiektów arcpy.Geometry
# UWAGA: SHAPE@X i SHAPE@Y działają tylko dla geometrii punktowych,
#        dlatego je usuwamy, bo linie mają wiele wierzchołków.
cursor = arcpy.da.SearchCursor(WarstwaLinie, ["SHAPE@"])

i = 0  # licznik obiektów

for row in cursor:
    geom = row[0]  # obiekt geometryczny linii
    print(f"--- Obiekt {i} ---")
    
    ListCoorOb = []
    # Iteracja po częściach (część = pojedyncza linia lub segment multipart)
    for part in geom:
        print("  Część obiektu:")
        
        # Iteracja po wierzchołkach danej części
        for pnt in part:
            if pnt:  # niektóre części mogą mieć None
                print(f"    Wierzchołek: X={pnt.X}, Y={pnt.Y}")
                ListCoorOb.append((pnt.X, pnt.Y))  # zapis do listy
    print(ListCoorOb)
    ListCoorLinie.append(ListCoorOb)
    i += 1

print(f"Liczba obiektów w warstwie: {i}, {len(ListCoorLinie)}")

# Dobre praktyki: usuwamy kursor, aby zwolnić blokadę do pliku .gdb
del cursor
