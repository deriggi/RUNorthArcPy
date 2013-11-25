class DBManager:

    def queryDatabase(self):
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
