import arcpy

arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"
WarstwaPKT = "R2014_OT_ADMS_P"

ListCoor = []
cursor = arcpy.da.SearchCursor(WarstwaPKT, ["SHAPE@X", "SHAPE@Y"])
for row in cursor:
    print(row)
    ListCoor += [[row[0]+1000, row[1]+2000]]
del cursor

NowaWarstwa = "R2014_OT_ADMS_P_przesu"
arcpy.management.CreateFeatureclass(arcpy.env.workspace, NowaWarstwa, "POINT", 
                                    "", "DISABLED", "DISABLED", 
                                    WarstwaPKT)

cursor = arcpy.da.InsertCursor(NowaWarstwa, ["SHAPE@X", "SHAPE@Y"])
for coor in ListCoor:
    cursor.insertRow(coor)

del cursor