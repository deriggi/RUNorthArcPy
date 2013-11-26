## ArcPy at RAMP UP North
Welcome to the RAMP UP North GIS Unit's GitHub Site! This site contains the Python examples, lessons,
and projects we will be using for this project. We are learning Python so that we can build the software
infrastrucutre required for the safayi registration integration task. Also Python is a great way to automate common
ArcGIS tasks

### Learning Python
Lessons for basic Python programming and introductory ArcPy are used to introduce the fundamentals. ArcPy has an 
extensive API so understanding basic Python command structures is necessary for building stable and reusable ArcPy
applications

#### First Lessons
The introductory lessons work through basic programming structures likes
  1. printing and variables
  ```python
      bicycles = 5
      s = "i have {0} bicycles".format(bicycles)
      print s

  ```
  2. string manipulation
  3. conditional statements
  4. loops

  ```python
    provinces = ['Balkh', 'Badakshan', 'Baghlan', 'Faryab', 'Jawzjan', 'Kunduz', 'Samangan', 'Takhar']
    for p in provinces:
      print 'a province name: {0}'.format(p)
  ```
  
  5. functions
  6. writing text files
  


#### ArcPy Assignments

The first assignment requires writing an arcpy script to iterate through spatial data, get the centroid, and write the
data out as json.


[1) Shapefile Centroid to JSON](https://docs.google.com/document/d/1paWDiVn_09vb8CHPGPbMIF_1BFhRGH1KVSTCe9DBGIM/edit)


```python
  #
  # This example prints the object id and the centroid of each shape in the shapefile.
  # It could be modified to print JSON
  #
  # ===============================
  # change this line
  layerpath = "C:/Users/jderiggi/Documents/afghramp/gis_data/Parcels_John.shp"
  # ===============================

  # use the current workspace
  mxd = arcpy.mapping.MapDocument("CURRENT")
        
  # add the layer to the bottom
  df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
  layerToAdd = arcpy.mapping.Layer(layerpath)
  arcpy.mapping.AddLayer(df,layerToAdd,"BOTTOM")

  # print attributes
  cursor = arcpy.da.SearchCursor(layerToAdd, ['@OID','SHAPE@TRUECENTROID'])
  for row in cursor:
    print 'ObjectID: {0}    Centroid: {1} '.format(row[0], row[1])
    
```





Assignment two requires the programmers to query the sql server database using attribute values of the spatial data


[2) Query SQL Server From ArcPy](https://docs.google.com/document/d/10GhARtr_xj9JQ7BSkvfF34Su0UA3i2ITnAm-oUzG3fE/edit?usp=sharing)

```python
  # change this line to point to your db connection
  sde_conn = arcpy.ArcSDESQLExecute(r"C:/DeRiggiComputer/ArcCatalog/Connection to DAIL13077.sde")
  
  # the sql query
  sql = "select PropertyID, District from IFMSDB.DBO.Property where District = {0} and Block = {1} and ParcelNo = {2}".format(1, 226, 4)          
  
  # the response
  sde_return = sde_conn.execute(sql)
  
```


In retrospect it would have been easier to do a CSV example first, but these json files are an important
part of the IFMS integration effort here

The JSON format can then be embedded into web applications as we do in the Web Mapping Assignments



#### Web Maping Assignments

In the web mapping assignments we use the json and/or csv files we created with arcpy to build some web based maps with
free open source tools like leaflet js


[1) JSON Points on a Map](https://docs.google.com/document/d/1XyVzYlqORZo7VEWlZOtqHNkyyKV1jiKAUseluYVKvW8/edit?usp=sharing)

```JavaScript
// a tiny json object!

{"centroid":[67.11519357832525,36.70581137062923]}
```

The second task introduces a site called geojson.io which makes it easy to make a web map from common spatial data
formats. Students modify their scripts to produce CSV files and then simply drag them onto the geojson.io page

[2) Creating CSV files and GeoJson.IO](https://docs.google.com/document/d/1n1tYgcQBd8I7Uxw94ChTBsWeGmwOZ8C7J5av8mxQ7aw/edit?usp=sharing)

