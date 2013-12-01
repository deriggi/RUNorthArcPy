import arcpy
import random

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
        districLayerParam = arcpy.Parameter(
            displayName="District Layer",
            name="districts",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        districtNumAttributeParam = arcpy.Parameter(
            displayName="District Number Attribute",
            name="distnumattribute",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        districtNumAttributeParam.filter.type = 'ValueList'

        blockLayerParam = arcpy.Parameter(
            displayName="Block Layer",
            name="blocks",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        blockNumAttributeParam = arcpy.Parameter(
            displayName="Block Number Attribute",
            name="blucknumattribute",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
        blockNumAttributeParam.filter.type = 'ValueList'


        parcelLayerParam = arcpy.Parameter(
            displayName="Parcel Layer",
            name="parcels",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input")

        parcelDistrictParam = arcpy.Parameter(
            displayName="District Field for the Parcel Layer",
            name="parceldistrictfield",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        parcelDistrictParam.filter.type = 'ValueList'

        parcelBlockParam = arcpy.Parameter(
            displayName="Block Field for the Parcel Layer",
            name="parcelblockfield",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
        parcelBlockParam.filter.type = 'ValueList'


        params = [districLayerParam, districtNumAttributeParam, blockLayerParam, blockNumAttributeParam, parcelLayerParam, parcelDistrictParam, parcelBlockParam]
        return params


    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        
        district = parameters[0] 
        if( district.altered and district.valueAsText != None and len(district.valueAsText) > 0 ):
            lm = LayerManager()
            parameters[1].filter.list = lm.getLayerFields(district.valueAsText)


        block = parameters[2] 
        if( block.altered and block.valueAsText != None and len(block.valueAsText) > 0 ):
            lm = LayerManager()
            parameters[3].filter.list = lm.getLayerFields(block.valueAsText)

        
        parcel = parameters[4] 
        if( parcel.altered and parcel.valueAsText != None and len(parcel.valueAsText) > 0 ):
            lm = LayerManager()
            parameters[5].filter.list = lm.getLayerFields(parcel.valueAsText)
            parameters[6].filter.list = lm.getLayerFields(parcel.valueAsText)

           


        return


    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        
        
        
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        p0 = parameters[0].valueAsText
        if p0 != None and len(p0) > 0 and p0.lower().find('parcel') == -1:
            parameters[0].setWarningMessage("must be a parcel layer")
            messages.addErrorMessage('must be a parcel layer') 
               

        intersector = Intersector()
        layermanager = LayerManager()

        districts = parameters[0].valueAsText
        districtNumAttribute = parameters[1].valueAsText

        blocks = parameters[2].valueAsText
        blockNumAttribute = parameters[3].valueAsText

        parcels = parameters[4].valueAsText 
        
        parcelDistrictAttributeName = parameters[5].valueAsText
        parcelBlockAttributeName = parameters[6].valueAsText
        
        



        # arcpy.MakeFeatureLayer_management(parcels,"parcels_layer")
        # arcpy.MakeFeatureLayer_management(blocks,"blocks_layer")

        blockOidName = layermanager.getLayerOIDName( blocks )
        parcelOidName = layermanager.getLayerOIDName( parcels )

        manyparcels = arcpy.da.SearchCursor(parcels ,[parcelOidName, parcelDistrictAttributeName, parcelBlockAttributeName])
        
        # todo, for each parcel check block and district attributes withintersections
        rm = RandomStringMaker()
        tempParcelsName = 'parcels_layer_{0}'.format(rm.getOne(5))
        arcpy.MakeFeatureLayer_management(parcels,tempParcelsName)
        # =================================
        for parcel in manyparcels:
            whereclause = arcpy.AddFieldDelimiters( parcels , parcelOidName ) + '= ' + str(parcel[0])

            arcpy.SelectLayerByAttribute_management(tempParcelsName, "NEW_SELECTION" , whereclause )
            

            # blocks
            # get block value for this parcel
            parcelsBlock = layermanager.getFirstAttributeValue(tempParcelsName, parcelBlockAttributeName, parcelOidName, parcel[0] )

            # is it actually in parcelsBlock?                                                       # have to ensure this is just a number
            blockwhereclause = arcpy.AddFieldDelimiters( blocks, blockNumAttribute ) + ' = ' + str( parcelsBlock )
            messages.addMessage(blockwhereclause)            
            response = intersector.isSelectedCentroidAWithinSpecificLayerB( tempParcelsName , blocks, blockNumAttribute, parcelsBlock )

            intersectsWithBlock = False

            if len(response) > 0:
                if int(parcelsBlock) == int(response[0]):
                    intersectsWithBlock = True
                messages.addMessage('parcel {0} intersects with block {1} but attribute says with {2}  {3} '.format(parcel[0], response[0], parcelsBlock, intersectsWithBlock))



            # districts
            # get district value for this parcel
            parcelsDistrict = layermanager.getFirstAttributeValue(tempParcelsName, parcelDistrictAttributeName, parcelOidName, parcel[0] )

            # is it actually in parcelsBlock?                                                           # have to ensure this is just a number
            distwhereclause = arcpy.AddFieldDelimiters( districts , districtNumAttribute ) + ' = ' + str( parcelsDistrict )
            messages.addMessage(distwhereclause)
            x = 1
            x=2
            x = x+2
            districtResponse = intersector.isSelectedCentroidAWithinSpecificLayerB( tempParcelsName, districts, districtNumAttribute, parcelsDistrict )

            intersectsWithDistrict = False

            if len(districtResponse) > 0:
                if int(parcelsDistrict) == int(districtResponse[0]):
                    intersectsWithDistrict = True
                messages.addMessage('parcel {0} intersects with district {1} but attribute says with {2}  {3} '.format(parcel[0], districtResponse[0], parcelsDistrict, intersectsWithDistrict))
            


        return


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


class Intersector:
    
    def isSelectedCentroidAWithinSpecificLayerB(self, selectedLayer, layerB , fieldname, fieldValue):
        layerManager = LayerManager()
        
        # centroid of selected layer
        geom = layerManager.getFirstSelectedTrueCentroidGeom(selectedLayer)
        
        # test centroid with layerB
        whereclause = arcpy.AddFieldDelimiters( layerB , fieldname ) + ' = ' + str( fieldValue )
        cursor = arcpy.da.SearchCursor( layerB , [fieldname, 'SHAPE@'], whereclause )
        response = []

        for row in cursor:
            if row[1] is not None and (row[1].contains(geom)):
                response.append(  str(row[0]) )

        return response

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

    
    def getLayerOIDName(self, layer):
        # Create a list of fields using the ListFields function
        fields = arcpy.ListFields(layer)

        # Iterate through the list of fields
        for field in fields:
            if field.type == 'OID':
                return field.name

        return ''

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