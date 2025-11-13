import arcpy

arcpy.env.workspace = r"C:\PG\ZMG_2025_26\ArcGIS_ZMG\ArcGIS_ZMG.gdb"
WarstwaPKT = "R2014_OT_ADMS_P"

cursor = arcpy.da.SearchCursor(WarstwaPKT, ["SHAPE@X", "SHAPE@Y"])
for row in cursor:
    print(row)
del cursor