import arcpy

arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"
WarstwaPKT = "R2014_OT_ADMS_P"

ListCoor = []
cursor = arcpy.da.SearchCursor(WarstwaPKT, ["SHAPE@X", "SHAPE@Y"])
for row in cursor:
    print(row)
    ListCoor += [row[0]+1000, row[1]+2000]
del cursor

arcpy.management.CreateFeatureclass("C:/output", "habitatareas.shp", "POLYGON", 
                                    "study_quads.shp", "DISABLED", "DISABLED", 
                                    "C:/workspace/landuse.shp")