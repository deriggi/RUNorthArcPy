import arcpy
import random
import sys
import os

class PNGMaker:

    def printLayerPaths(self):
        lm = LayerManager()
        layer = lm.getLayer(0)
        print layer.dataSource

    def makeReportForSingleFeature(self,  workspace="CURRENT"):
        # self.charsetInfo()

        lm = LayerManager(workspace)
        
        # todo, get the layer with the name parcel in it
        firstLayer = lm.getLayer(0)
        rm = RandomStringMaker()

        # the base directory
        baseDir = 'C:/Users/jderiggi/Documents/afghramp/'

        # get the attributes for the selected layer
        attributes = lm.getLayerAttribute(firstLayer, ['Dist_No', 'Block_Numb', 'Parcel_ID' ])
        
        district    = str(attributes[0])
        block       = str(attributes[1])
        parcel      = str(attributes[2])

        print 'attributes for this file '
        print '\tdistrict:\t'   +       district 
        print '\tblock:\t\t'    +       block 
        print '\tparcel:\t\t'   +       parcel  

        folderName = 'dist' + district + '_' + 'block' + block + '_' + 'parcel' + parcel
        fullReportPath = baseDir + folderName
        
        # make the folder if it does not exist
        if not os.path.exists(fullReportPath):
            os.makedirs(fullReportPath)
        
        # zoom to extent of selected and export png
        lm.zoomAndExportPNG(fullReportPath + '/' + rm.getOne(5) + 'zoom_3dot5', 1.3)
        lm.zoomAndExportPNG(fullReportPath + '/' + rm.getOne(5) + 'zoom_15dot5', 15.5)
        lm.zoomAndExportPNG(fullReportPath + '/' + rm.getOne(5) + 'zoom_30dot5', 30.5)

        # query IFMS for this data
        db = DBManager()
        print 'querying for {0}, {1}, {2}'.format(district,block,parcel)

        # handle the response
        response = db.queryProperty(district, block, parcel)
        rdict = self.convertPropertyResponseToDict(response)

        print 'report being generated to: ' + fullReportPath
        self.appendToFile(fullReportPath + '/report.txt',  self.convertDictToReport(rdict)  )

    def convertPropertyResponseToDict(self, response):
        responseDict = {}
        print 'response out is ' + str(response)

        if isinstance(response, list):
            for record in response:
                PropertyID = record[0]
                SerialNumber = record[1]
                PropertyRegNo = record[2]
                propertyType = unicode(record[3])
                propertyUsage = unicode(record[4])
                QabalaNo = record[5]
                District = record[6]
                area = unicode(record[7])
                guzer = record[8]
                block = record[9]

                streetNameOrNo = unicode(record[10])
                parcel = unicode(record[11])

                northSide = unicode(record[12])
                southSide = unicode(record[13])
                eastSide = unicode(record[14])
                westSide = unicode(record[15])

                insertedDate = record[17]
                
                responseDict['Property ID'] = str(PropertyID)
                responseDict['Serial Number'] = str(SerialNumber)

                responseDict['Property Reg Number'] = str(PropertyRegNo)
                
                responseDict['Property Type'] = propertyType
                responseDict['Property Usage'] = propertyUsage
                responseDict['Area'] = area
                responseDict['QabalaNo'] = str(QabalaNo)
                responseDict['Guzer'] = str(guzer)
                responseDict['Street Name or No'] = streetNameOrNo
                responseDict['North Side'] = northSide
                responseDict['South Side'] = southSide
                responseDict['East Side'] = eastSide
                responseDict['West Side'] = westSide
        else:
            print 'response is not a list'
            print response
        return responseDict


    def convertDictToReport(self, r):
        base = ''
        
        for key, val in r.items():
            base += key + ' :\t ' + val + '\n'

        return base

        

    def appendToFile(self, filePath, line):
        fileHandle = open(filePath, 'a')
        fileHandle.write((line + '\n').encode('utf8'));

        fileHandle.close()
        

    def makePngForEachFeature(self, layerpath, workspace="CURRENT"):
        
        lm = LayerManager(workspace)

		# get the oid for this name
        oidName = lm.getLayerOIDName(layerpath)

        rows = arcpy.da.SearchCursor(layerpath,[oidName])

        counter = 0

        theLayer = arcpy.mapping.Layer(layerpath)
        # theLayer = lm.getLayer(0)
        
        rm = RandomStringMaker()

        # lm.addLayerToCurrent(theLayer)

        # =====
        # this works
                # whereclause = arcpy.AddFieldDelimiters( theLayer , oidName ) + '= ' + str(5)
                
                # print whereclause

                # randomname = rm.getOne(5);

                # arcpy.MakeFeatureLayer_management(layerpath, randomname)

                # arcpy.SelectLayerByAttribute_management(randomname, "NEW_SELECTION" , whereclause )
                    
                # lm.zoomAndExportPNG('C:/Users/jderiggi/Documents/afghramp/arcgisProjects/' + rm.getOne(5) )

                # lm.removeLayer(theLayer)

        #========

        whereclause = arcpy.AddFieldDelimiters( theLayer , oidName ) + '= ' + str(5)        
        print whereclause
        randomname = rm.getOne(5);
        arcpy.SelectLayerByAttribute_management(lm.getLayer(0), "NEW_SELECTION" , whereclause )
        lm.zoomAndExportPNG('C:/Users/jderiggi/Documents/afghramp/arcgisProjects/' + rm.getOne(5) )
        

        #for record in rows:
            
            # works!
            
            #whereclause = arcpy.AddFieldDelimiters( theLayer , oidName ) + '= ' + str(record[0])

            # the way to add pats to where clause
            ## whereclause += ' and ' + arcpy.AddFieldDelimiters( theLayer , 'Shape_Le_1' ) + '= ' + str(122.619452)
            
            #print whereclause

            
            #arcpy.SelectLayerByAttribute_management(theLayer, "NEW_SELECTION" , whereclause )
            
            #lm.zoomAndExportPNG('C:/Users/jderiggi/Documents/afghramp/arcgisProjects/' + rm.getOne(5) )
            
            #counter += 1

        #lm.removeLayer(theLayer)
        
        #print counter


    def makePngForEachFeatureAtIndex(self, layerIndex, workspace="CURRENT"):
            
            lm = LayerManager(workspace)
            theLayer = lm.getLayer(layerIndex)
            arcpy.SelectLayerByAttribute_management(theLayer, "CLEAR_SELECTION")

            # get the oid for this name
            oidName = lm.getLayerOIDName(theLayer)
            rows = arcpy.da.SearchCursor(theLayer,[oidName])
            counter = 0
            rm = RandomStringMaker()

            for record in rows:
                whereclause = arcpy.AddFieldDelimiters( theLayer , oidName ) + '= ' + str(record[0])        
                print whereclause
                arcpy.SelectLayerByAttribute_management(theLayer, "NEW_SELECTION" , whereclause )
                lm.zoomAndExportPNG('C:/Users/jderiggi/Documents/afghramp/arcgisProjects/' + rm.getOne(5) )
            del lm
            del theLayer



class DBManager:

    def queryProperty(self, district, block, parcel):
        try:
            # Database Connections/balrog.odc/vtest.COUNTIES
            # table = ["IFMSDB.DBO.%Property"]
            sde_conn = arcpy.ArcSDESQLExecute(r"C:\\Users\\Administrator\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\Connection to DAIL13077.sde")
            sql = "select * from IFMSDB.DBO.Property where District = {0} and  Block = {1}  and ParcelNo = {2}".format(district,  block, parcel)

            #Pass the SQL statement to the database.
            sde_return = sde_conn.execute(sql)

            # table = ["C:\\Users\Administrator\\AppData\\Roaming\\ESRI\\Desktop10.2\\ArcCatalog\\Connection to DAIL13077.sde"]
            return sde_return;

        except Exception, e:
            # If an error occurred, print line number and error message
            sde_return=false
            import traceback, sys
            tb = sys.exc_info()[2]
            print "Line %i" % tb.tb_lineno
            print e.message

class LayerManager:
    def __init__(self, wrkspc="CURRENT"):
        self.workspace = wrkspc

    def zoomAndExportPNG(self,outputpath, scaleby=1):
        mxd = arcpy.mapping.MapDocument(self.workspace)
        df = arcpy.mapping.ListDataFrames(mxd)[0]
        lyr = arcpy.mapping.ListLayers(mxd)[0]
        ext = lyr.getSelectedExtent()
        df.extent = ext
        df.scale = df.scale * scaleby
        arcpy.mapping.ExportToPNG(mxd, outputpath + ".png")
        print 'done exporting'

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
        #singleBlockLayerName = newname + r.getOne(6) 
        #arcpy.CopyFeatures_management(layer, outwrkspace+"/" + singleBlockLayerName )
        #self.addLayerToCurrent(outwrkspace + "/" + singleBlockLayerName )

    def addLayerToCurrent(self, layer):
        mxd = arcpy.mapping.MapDocument(self.workspace)
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        arcpy.mapping.AddLayer(df, layer)

    def addLayerPathToCurrent(self, layerpath):
        mxd = arcpy.mapping.MapDocument(self.workspace)
        
        # make ListLayers instead?
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]

        layerToAdd = arcpy.mapping.Layer(layerpath)
        arcpy.mapping.AddLayer(df,layerToAdd,"BOTTOM")

    def getLayerCount(self):
        mxd = arcpy.mapping.MapDocument(self.workspace)
        layers = arcpy.mapping.ListLayers(mxd)

        return len(layers)

    def removeLayer(self, layer):
        mxd = arcpy.mapping.MapDocument(self.workspace)
        df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
        arcpy.mapping.RemoveLayer(df, layer)

    def getLayer(self, index):
        mxd = arcpy.mapping.MapDocument(self.workspace)
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

    
    def getLayerAttribute(self, layer, attributenames):
        cursor = arcpy.da.SearchCursor( layer, attributenames )
        attributeVals = []
        for row in cursor:
            for x in range (0, len(attributenames)):
                attributeVals.append(row[x])

        return attributeVals


    def getLayerAttributeByIndex(self, layerindex, attributenames):
        mxd = arcpy.mapping.MapDocument(self.workspace)
        df = arcpy.mapping.ListLayers(mxd)
        lyr = df[layerindex]
        cursor = arcpy.da.SearchCursor( lyr, attributenames )
        attributeVals = []
        for row in cursor:
            for x in range (0, len(attributenames)):
                attributeVals.append(row[x])

        return attributeVals


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





maker = PNGMaker()

# maker.printLayerPaths()

# maker.makePngForEachFeature('C:/Users/jderiggi/Documents/afghramp/gis_data/GIS_ Geodatabase.gdb/Kunduz_Data/Kunduz_Parcels', 'C:/Users/jderiggi/Documents/afghramp/arcgisProjects/Blank.mxd')
# maker.makePngForEachFeatureAtIndex('C:/Users/jderiggi/Documents/afghramp/gis_data/Parcels_John_reproj.shp')
# maker.makePngForEachFeatureAtIndex(0)
maker.makeReportForSingleFeature()

