import arcpy

# the line to change
layerpath = "C:/Users/jderiggi/Documents/afghramp/gis_data/Parcels_John.shp"
output = "C:/Users/jderiggi/Documents/afghramp/gis_data/Parcels_John_selected.shp"

# add a layer to the current workspace
mxd = arcpy.mapping.MapDocument("CURRENT")
        
# add the layer to the bottom
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
layerToAdd = arcpy.mapping.Layer(layerpath)
arcpy.mapping.AddLayer(df,layerToAdd,"BOTTOM")

# select by area
whereclause = '"Shape_Area" > 400' 
arcpy.Select_analysis(layerToAdd, output , whereclause)


