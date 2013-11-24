import arcpy


def runAll():
	# the line to change
	layerPath = "C:/Users/jderiggi/Documents/afghramp/gis_data/Parcels_John_reproj.shp"

	fidName = "FID"

	rows = arcpy.da.SearchCursor(layerpath,[fidName])

	counter = 0

	theLayer = arcpy.mapping.Layer(layerpath)

	addLayerPathToCurrent(layerpath)

	for record in rows:
	    # whereclause = arcpy.AddFieldDelimiters( theLayer , fidName ) + '= ' + str(record[0])
	    whereclause = '"FID" = ' + str(record[0])
	    
	    print whereclause
	    
	    arcpy.SelectLayerByAttribute_management(theLayer, "NEW_SELECTION" , whereclause )
	    arcpy.RefreshActiveView()
	    df.zoomToSelectedFeatures()
	    arcpy.RefreshActiveView()
	    arcpy.mapping.ExportToPNG(mxd, 'C:/Users/jderiggi/Documents/afghramp/arcgisProjects/bigparcels' + str(record[0]) )
	    arcpy.SelectLayerByAttribute_management(theLayer, "CLEAR_SELECTION")
	    

	    # removeLayer(theLayer)

def addLayerPathToCurrent( layerpath):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    
    # make ListLayers instead?
    df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

    layerToAdd = arcpy.mapping.Layer(layerpath)
    arcpy.mapping.AddLayer(df,layerToAdd,"BOTTOM")


def zoomAndExportPNG(outputpath):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd)[0]
    lyr = arcpy.mapping.ListLayers(mxd)[0]
    ext = lyr.getSelectedExtent()
    df.extent = ext
    #df.scale = df.scale * scaleby
    arcpy.mapping.ExportToPNG(mxd, outputpath + ".png")
    print 'done exporting'

def removeLayer( layer):
    mxd = arcpy.mapping.MapDocument("CURRENT")
    df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
    arcpy.mapping.RemoveLayer(df, layer)



runAll();

