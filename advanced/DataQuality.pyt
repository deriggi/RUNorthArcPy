import arcpy


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="District Layer",
            name="districts",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        param1 = arcpy.Parameter(
            displayName="Block Layer",
            name="blocks",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        param2 = arcpy.Parameter(
            displayName="Parcel Layer",
            name="parcels",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        params = [param0, param1, param2]
        return params


    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        intersector = Intersector()
        layermanager = LayerManager()

        parcels = parameters[1].valueAsText 
        blocks = parameters[0].valueAsText

        arcpy.MakeFeatureLayer_management(parcels,"parcels_layer")
        arcpy.MakeFeatureLayer_management(blocks,"blocks_layer")

        blockOidName = layermanager.getLayerOIDName( "blocks_layer" )
        parcelOidName = layermanager.getLayerOIDName( "parcels_layer" )

        manyparcels = arcpy.da.SearchCursor("parcels_layer" ,[parcelOidName])
        
        

        for parcel in manyparcels:
            whereclause = arcpy.AddFieldDelimiters( "parcels_layer" , parcelOidName ) + '= ' + str(parcel[0])

            arcpy.SelectLayerByAttribute_management("parcels_layer", "NEW_SELECTION" , whereclause )
            
            response = intersector.isSelectedCentroidAWithinLayerB( "parcels_layer" , "blocks_layer", blockOidName )

            if len(response) > 0:
                messages.addMessage('parcel {0} intersects with block {1}'.format(parcel[0], response[0]))
            else:
                messages.addMessage('{0} NOT intersect'.format(""))

        return


class LayerManager:

    def getFirstSelectedTrueCentroidGeom(self, layer):
        centroid = self.getFirstSelectedTrueCentroid(layer)
        point = arcpy.Point(centroid[0], centroid[1])
        
        return point

    def getFirstSelectedTrueCentroid(self, layer):
        print 'trying ' + str(layer);
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


class Intersector:
    
    def isSelectedCentroidAWithinLayerB(self, selectedLayer, layerB , fieldname):
        layerManager = LayerManager()
        
        geom = layerManager.getFirstSelectedTrueCentroidGeom(selectedLayer)
        cursor = arcpy.da.SearchCursor( layerB , [fieldname, 'SHAPE@'] )
        response = []

        for row in cursor:
            if row[1] is not None and (row[1].contains(geom)):
                response.append(  str(row[0]) )

        return response

    # list the polygons that contain the centroid
    def isPointWithinNextLayer(self, selectedLayer, intersectlayerindex , fieldname):
        layerManager = LayerManager()
        districts = layerManager.getLayer(intersectlayerindex)
        geom = layerManager.getFirstSelectedTrueCentroidGeom(selectedLayer)
        cursor = arcpy.da.SearchCursor( districts , [fieldname, 'SHAPE@'] )
        response = []

        for row in cursor:
            if row[1] is not None and (row[1].contains(geom)):
                response.append(  str(row[0]) )

        return response
        

    def getBlockForSelectedParcel(self, selectedFeature):
        cursor = arcpy.da.SearchCursor(selectedFeature, ['OID@', 'SHAPE@'] )
        fields = cursor.fields

        for row in cursor:        
            isPointWithinNextLayer( row[1])
