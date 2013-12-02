import random

#===========================
'''

	This updates a new column on the parcels called pk_prop which enables the single-field join 
	to an external table in arcgis


'''
#===========================



class RandomStringMaker:
    def __init__(self):
        self.letters = []
        self.letters= ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

    def getOne(self, size):
        s = ''
        for i in range(0, size):
            s += str(self.getAlphaOrNumerica())
        return s

    def getAlphaOrNumerica(self):
        if random.randint(0,1) > 0:
            return self.getRandomLetter()
        return random.randint(0,9)


    def getRandomLetter(self):
        return self.letters[random.randint(0,25)]

class LayerManager:

    def getFirstSelectedTrueCentroidGeom(self, layer):
        centroid = self.getFirstSelectedTrueCentroid(layer)
        point = arcpy.Point(centroid[0], centroid[1])
        
        return point

    def getFirstAttributeValue(self, layer, attributename, oidname, oidvalue):
        whereclause = arcpy.AddFieldDelimiters( layer , oidname ) + '= ' + str( oidvalue )
        cursor = arcpy.da.SearchCursor(layer, attributename)

        for row in cursor:
            return row[0]

        return

    def getFirstSelectedTrueCentroid(self, layer):
        cursor = arcpy.da.SearchCursor( layer , ['SHAPE@TRUECENTROID'] )
        for row in cursor:
            return row[0]

    def getLayerOIDName(self, layer):
        # Create a list of fields using the ListFields function
        fields = arcpy.ListFields(layer)

        # Iterate through the list of fields
        for field in fields:
            if field.type == 'OID':
                return field.name

        return ''

    def getLayerFields(self, layer):
        # Create a list of fields using the ListFields function
        fields = arcpy.ListFields(layer)
        fieldsList = []
        # Iterate through the list of fields
        for field in fields:
            fieldsList.append(field.name)

        return fieldsList

class DBManager:
	def queryDatabase(self, connection_string, district, block, parcel):
        
		try:
            
			sde_conn = arcpy.ArcSDESQLExecute(connection_string)

			# sql = "select * from IFMSDB.DBO.Property where District = {0} and Block = {1} and ParcelNo = {2}".format(district, block, parcel)

			sql = 'select  PropertyID from IFMSDB.dbo.Property where District = {0} and Block = {1} and ParcelNo = {2} and CHARINDEX(\'-\',PropertyRegNo) = 0'.format(district, block, parcel)
            
			sde_return = sde_conn.execute(sql)
			propertyId = None

			if isinstance(sde_return, list):
				print "BAD: MULTIPLE RECORDS!" 
				print "Number of rows returned by query: {0} rows".format(len(sde_return))	
				for record in sde_return:
					propertyID = record[0]   
					print "list item property: {0}".format(record[0])
				propertyID = None

			elif sde_return is not None and sde_return is not True:
				propertyId = sde_return
				
				print "single property: {0}".format(sde_return)
            		

			del sde_conn


		except Exception, e:
            # If an error occurred, print line number and error message
			import traceback, sys
			tb = sys.exc_info()[2]
			print "Line %i" % tb.tb_lineno
			print e.message

		return propertyId

def testDB():

	district = 1;
	block = 244;
	parcel = 2

	db = DBManager()
	propertyID = db.queryDatabase(district, block, parcel)

	if propertyID is not None:
		print '{0} is the pk for {1} {2} {3}'.format(propertyID, district, block, parcel)


def run_it():
	# ========================================================
	# sde connection - change this to your path
	# sde_conn = arcpy.ArcSDESQLExecute(r"C:\\Users\\Administrator\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\Connection to DAIL13077.sde")
	parcels = 'C:/Users/jderiggi/Documents/afghramp/gis_data/Parcels_John_reproj.shp'
	connection_string = r'C:/Users/Administrator/AppData/Roaming/ESRI/Desktop10.2/ArcCatalog/Connection to DAIL13077.sde'
	# ========================================================



	rm = RandomStringMaker()
	tempParcelsName = 'parcels_layer_{0}'.format(rm.getOne(5))
	#arcpy.MakeFeatureLayer_management(parcels,tempParcelsName)

	lm = LayerManager()
	parcelOidName = lm.getLayerOIDName( parcels )

	manyparcels = arcpy.da.UpdateCursor( parcels , [ parcelOidName, 'prop_pk', 'Dist_No', 'Block_Numb', 'Parcel_ID'])
	
	db = DBManager()

	for parcel in manyparcels:
		
		# whereclause = arcpy.AddFieldDelimiters( parcels , parcelOidName ) + ' = ' + str( parcel[0] )
		print 'on parcel oid {0}  {1}  {2}  {3}  {4}'.format(parcel[0], parcel[1], parcel[2], parcel[3], parcel[4])

		pk = db.queryDatabase(connection_string, parcel[2],parcel[3],parcel[4])
		if pk is not None:
			parcel[1] = pk
			manyparcels.updateRow(parcel)

	

run_it()
