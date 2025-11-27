import arcpy

# Ustawienie geobazy roboczej
arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"

# Nazwa warstwy (feature class)
WarstwaPoligonowa = "Budynek_01"

# Lista na współrzędne (jeśli chcesz je później wykorzystać)
ListCoorPoly = []
ListCoorCentr = []

# SearchCursor – odczyt geometrii (SHAPE@) w postaci obiektów arcpy.Geometry
# UWAGA: SHAPE@X i SHAPE@Y działają tylko dla geometrii punktowych,
#        dlatego je usuwamy, bo linie mają wiele wierzchołków.
cursor = arcpy.da.SearchCursor(WarstwaPoligonowa, ["SHAPE@", "SHAPE@XY"])

i = 0  # licznik obiektów

for row in cursor:
    geom = row[0]  # obiekt geometryczny poligonowy
    centr = row[1]
    print(centr)
    ListCoorCentr.append(centr)
    # print(f"--- Obiekt {i} ---")
    
    ListCoorOb = []
    # Iteracja po częściach (część = pojedyncza poligonu lub segment multipart)
    for part in geom:
        # print("  Część obiektu:")
        ListCoorPart = []
        # Iteracja po wierzchołkach danej części
        for pnt in part:
            print(pnt)
            if pnt:  # niektóre części mogą mieć None
                # print(f"    Wierzchołek: X={pnt.X}, Y={pnt.Y}")
                newX = (pnt.X - centr[0])*2
                newY = (pnt.Y - centr[1])*2
                ListCoorPart.append((newX, newY))  # zapis do listy
            else:
                ListCoorOb.append(ListCoorPart)
                ListCoorPart = []
        ListCoorOb.append(ListCoorPart)
    # print(ListCoorOb)
    ListCoorPoly.append(ListCoorOb)
    i += 1

print("Pierwszy obiekt:", ListCoorPoly[0])
print("Pierwsza część pierwszego obiektu:", ListCoorPoly[0][0])
print(f"Liczba obiektów w warstwie: {i}, {len(ListCoorPoly)}")

# Dobre praktyki: usuwamy kursor, aby zwolnić blokadę do pliku .gdb
del cursor



#############################################################################################
## budowanie warstwy poligonowej z dziurą
#############################################################################################
NowaWarstwa = "Budynek_01_nowy_02"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, NowaWarstwa, "POLYGON", 
                                    "", "DISABLED", "DISABLED", 
                                    WarstwaPoligonowa)

cursor = arcpy.da.InsertCursor(NowaWarstwa, ["SHAPE@"])
array = arcpy.Array() # Pusty obiekt na zbieranie wszystkich wierzchołków linii
part = arcpy.Array()
pnt = arcpy.Point() # Pusty obiekt na zapisywanie współrzednych wierzchołka jako PUNKT
i = 0
for Ob in ListCoorPoly:
    centr = ListCoorCentr[i]
    for Cze in Ob:
        for Wie in Cze:
            pnt.X, pnt.Y = Wie[0] + centr[0], Wie[1] + centr[1]
            array.add(pnt)
        part.add(array)
        array.removeAll()
    pol = arcpy.Polygon(part)
    part.removeAll()
    cursor.insertRow([pol])
    i += 1
del cursor


