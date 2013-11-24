
# the line to change
layerpath = "C:/Users/jderiggi/Documents/afghramp/gis_data/Parcels_John.shp"


# add a layer to the current workspace
mxd = arcpy.mapping.MapDocument("CURRENT")
        
# add the layer to the bottom
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
layerToAdd = arcpy.mapping.Layer(layerpath)
arcpy.mapping.AddLayer(df,layerToAdd,"BOTTOM")

# print attributes
cursor = arcpy.da.SearchCursor(layerToAdd, ['Shape_Area', 'OID@', 'SHAPE@TRUECENTROID'])
for row in cursor:
	print str(row[0]) + ' ' + str(row[1]) + ' ' + str(row[2])


