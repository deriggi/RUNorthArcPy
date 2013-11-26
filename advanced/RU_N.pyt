import arcpy
import os
import random


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [Tool_2, Tool ]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "RU-N Setup"
        self.description = ""
        self.canRunInBackground = False
        self.workspace = ''

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Parcel Layer",
            name="parcels",
            # datatype="GPFeatureLayer",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input")


        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Block Layer",
            name="blocks",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        param1.filter.type = 'ValueList'

        params = [param0, param1]
        return params


    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        layerManager = LayerManager()
        p0 = parameters[0]
        if p0.valueAsText != None and len(p0.valueAsText) > 0:
            self.workspace = p0.valueAsText
            names = layerManager.getFeatureNames(p0.valueAsText)
            parameters[1].filter.list = names

        
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        wouldBeParcelPath = parameters[0].valueAsText + '\\' +parameters[1].valueAsText         
        lm = LayerManager()
        names = lm.getFullFeatureNames(parameters[0].valueAsText)
        pathToParcel = ''

        for name in names:
            if name.find(parameters[1].valueAsText) != -1 and name.find('Parcel') != -1:
                pathToParcel = name


        # parcels = parameters[0].valueAsText
        # blocks = parameters[1].valueAsText
        # adder = LayerManager()
        # adder.addLayerToCurrent(parcels)
        
        if len(pathToParcel) > 0:
            lm.addLayerToCurrent(pathToParcel)

        messages.addMessage('\n')
        messages.addMessage('would like to show ' + pathToParcel)
        messages.addMessage('\n')
        return


class Tool_2(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "RU-N Analyze"
        self.description = " intersect with other layers"
        self.canRunInBackground = False


    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        # param0 = arcpy.Parameter(
        #     displayName="Province: Choose Balkh, Kunduz, Samangan..",
        #     name="parcels",
        #     # datatype="GPFeatureLayer",
        #     datatype="GPString",
        #     parameterType="Required",
        #     direction="Input")

        # param0.filter.type = 'ValueList'
        # param0.filter.list = ['Balkh', 'Kunduz', 'Samangan']

        # params = [param0]
        params = []
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
        
        layerManager = LayerManager()
        
        # get layer 0, then derive path to layer 1, layer 2, then add them  
        wrkspacePath = layerManager.getLayer(0).workspacePath
        dataSource = layerManager.getLayer(0).dataSource
        
        messages.addMessage("loading " + wrkspacePath)
        messages.addMessage("loading " + dataSource)

        layerOne = layerManager.replaceEndPathItem(dataSource, 'Blocks')
        messages.addMessage('trying to add layer ' + layerOne)
        layerManager.addLayerToCurrent(layerOne)

        layerTwo = layerManager.replaceEndPathItem(dataSource, 'Districts')
        messages.addMessage('trying to add layer ' + layerTwo)
        layerManager.addLayerToCurrent(layerTwo)        

        intersector = Intersector()

        blocksLayer = layerManager.getLayer(1)
        districtsLayer = layerManager.getLayer(2)
        
        blockOIDField =  layerManager.getLayerOIDName(blocksLayer)
        districtOIDField = layerManager.getLayerOIDName(districtsLayer)

        blockResponse = intersector.isPointWithinNextLayer(layerManager.getLayer(0) , 1, blockOIDField )
        districtResponse = intersector.isPointWithinNextLayer(layerManager.getLayer(0), 2, districtOIDField )
        
        # select intersecting feature and copy
        if len(blockResponse) > 0:
            whereclause_b = arcpy.AddFieldDelimiters(blocksLayer, blockOIDField) + '= ' + blockResponse[0]
            layerManager.addSelectedFeature(whereclause_b, blocksLayer, 'blocksLayer_', wrkspacePath)

        if len(districtResponse) > 0:
            whereclause_d = arcpy.AddFieldDelimiters(districtsLayer, districtOIDField) + '= ' + districtResponse[0]
            layerManager.addSelectedFeature(whereclause_d, districtsLayer, 'districtsLayer_', wrkspacePath)


        for r in blockResponse:
            messages.addMessage("intersects with block: " + r)

        for d in districtResponse:
            messages.addMessage("intersects with district: " + d)

        parcelAttributes = layerManager.getLayerAttribute(0 , ['OID@'] )

        db = DBManager()

        for p in parcelAttributes:
            dbResponse = db.queryDatabase(12)

            if isinstance(dbResponse, list):
                for record in dbResponse:
                    messages.addMessage('from db: ' + str(record[1]))
            else:
                messages.addMessage('nothing from db')

            messages.addMessage("for parcel: " + str(p))

        layerManager.removeLayer(blocksLayer)
        layerManager.removeLayer(districtsLayer)

        return




class LayerManager:

    def getLayerOIDName(self, layer):
        # Create a list of fields using the ListFields function
        fields = arcpy.ListFields(layer)

        # Iterate through the list of fields
        for field in fields:
            if field.type == 'OID':
                return field.name

        return ''


    def printLayerNameFields(self, layer):
        for field in fields:
            # Print field properties
            print("Field:       {0}".format(field.name))
            print("Alias:       {0}".format(field.aliasName))
            print("Type:        {0}".format(field.type))
            print("Is Editable: {0}".format(field.editable))
            print("Required:    {0}".format(field.required))
            print("Scale:       {0}".format(field.scale))
            print("Precision:   {0}".format(field.precision))


    # select a lone feature by attribute, copy it and add it as a layer
    def addSelectedFeature(self,whereclause, layer,newname,outwrkspace):
        arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION" , whereclause )
        r = RandomStringMaker()
        singleBlockLayerName = newname + r.getOne(6) 
        arcpy.CopyFeatures_management(layer, outwrkspace+"/" + singleBlockLayerName )
        self.addLayerToCurrent(outwrkspace + "/" + singleBlockLayerName )


    def addLayerToCurrent(self, layerpath):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        
        # make ListLayers instead?
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

        layerToAdd = arcpy.mapping.Layer(layerpath)
        arcpy.mapping.AddLayer(df,layerToAdd,"BOTTOM")

    def getLayerCount(self):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        layers = arcpy.mapping.ListLayers(mxd)

        return len(layers)

    def removeLayer(self, layer):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        arcpy.mapping.RemoveLayer(df, layer)

    def getLayer(self, index):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        layers = arcpy.mapping.ListLayers(mxd)
        return layers[index]

    def getFirstSelectedShape(self, layer):
        cursor = arcpy.da.SearchCursor( layer , ['SHAPE@'] )
        for row in cursor:
            return row[0]
    def getFirstSelectedTrueCentroidGeom(self, layer):
        centroid = self.getFirstSelectedTrueCentroid(layer)
        point = arcpy.Point(centroid[0], centroid[1])
        
        return point

    def getFirstSelectedTrueCentroid(self, layer):
        cursor = arcpy.da.SearchCursor( layer , ['SHAPE@TRUECENTROID'] )
        for row in cursor:
            return row[0]

    def getFullFeatureNames(self, workspace):
        
        feature_classes = []
        for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype="FeatureClass"):
            for filename in filenames:
                fullFeaturePath = os.path.join(dirpath, filename)
                if len( fullFeaturePath )> 0:
                    feature_classes.append(fullFeaturePath)

        return feature_classes

    def getFeatureNames(self, workspace):
        
        feature_classes = []
        for dirpath, dirnames, filenames in arcpy.da.Walk(workspace, datatype="FeatureClass"):
            for filename in filenames:
                fullFeaturePath = os.path.join(dirpath, filename)
                part = self.stripAFromB(workspace, fullFeaturePath)
                part = self.getFirstNonSlashedPart(part)
                if len(part )> 0:
                    feature_classes.append(part)


        return feature_classes

    def stripAFromB(self, partA, partB):
        # get only the _Data names that are after the db name
        parsedString = None

        index = partB.find(partA)
        if index != -1:
            parsedString = partB[len(partA) + index:]
        else:
            parsedString = partB

        return parsedString

    def getFirstNonSlashedPart(self, target):
        parts = target.split('\\')
        if len(parts) > 1:
            return parts[1]

        return parts

    def replaceEndPathItem(self, target, replacement):
        lastIndexOfSlash = target.rfind('\\')
        endToken = target[lastIndexOfSlash+1:]
        prefix = endToken[ 0 : endToken.find('_') ]
        returnString = target[0:lastIndexOfSlash] + '\\' + prefix + '_' + replacement

        return returnString 

    def getLayerAttribute(self, layerindex, attributenames):
        mxd = arcpy.mapping.MapDocument("CURRENT")
        df = arcpy.mapping.ListLayers(mxd)
        lyr = df[layerindex]
        cursor = arcpy.da.SearchCursor( lyr, attributenames )
        attributeVals = []
        for row in cursor:
            for x in range (0, len(attributenames)):
                attributeVals.append(row[x])

        return attributeVals



class Intersector:
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


class DBManager:

    def queryDatabase(self, propertyid):
        try:
            
            sde_conn = arcpy.ArcSDESQLExecute(r"C:\\Users\\Administrator\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\Connection to DAIL13077.sde")
            
            sql = "select PropertyID, District from IFMSDB.DBO.Property where District = {0} and  Block = {1}  and ParcelNo = {2}".format(1, 226, 4)

            
            sde_return = sde_conn.execute(sql)
                        
            return sde_return;

        except Exception, e:
            # If an error occurred, print line number and error message
            import traceback, sys
            tb = sys.exc_info()[2]
            print "Line %i" % tb.tb_lineno
            print e.message



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
