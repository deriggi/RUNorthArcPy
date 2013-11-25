import arcpy

# ============
# parameters
# ============
shape_path = "C:/Users/jderiggi/Documents/afghramp/gis_data/Parcels_John.shp"
minimum = 400
# end parameters


rows = arcpy.da.SearchCursor(shape_path,
                          ['Shape_Area', 'SHAPE@TRUECENTROID'])

count = 0
total_count = 0
for singleRow in rows:

	total_count  = total_count + 1
	
	area = float( singleRow[0] )
	center = singleRow[1]

	if area > minimum:
		count  = count + 1
		print "{0}   {1}".format(area, center)


print 'out of {0} parcels, there are {1} parcels with area greater than {2} '.format(total_count, count, minimum)