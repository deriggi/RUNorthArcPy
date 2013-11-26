# ArcPy at RAMP UP North
Welcome to the RAMP UP North GIS Unit's GitHub Site! This site contains the Python examples, lessons,
and projects we will be using for this project. We are learning Python so that we can build the software
infrastrucutre required for the safayi registration integration task. Also Python is a great way to automate common
ArcGIS tasks

## Learning Python
Lessons for basic Python programming and introductory ArcPy are used to introduce the fundamentals. ArcPy has an 
extensive API so understanding basic Python command structures is necessary for building stable and reusable ArcPy
applications

## 1.0 First Lessons
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
  
[code for the first lessons track](https://github.com/deriggi/RUNorthArcPy/tree/master/lessons/py_0)

## 2 ArcPy Assignments

### Project 2.1 - Write Centroids of a Shapefile to JSON
Use ArcPy to develop a system for converting a shapefile into JSON. This is going to be used for the IFMS integration!
Write an arcpy script to iterate through spatial data, get the centroid, and write the result out as json.

The output does not need to look exactly like the example but it must have two parts:

   1. a centroid element: the center point of the parcel
   2. 2. properties element:

It must be valid JSON.

Example:
```JavaScript
{
 "centroid": [
   67.115193578325,
   36.705811370629
 ],
 "properties": {
   "Parcel_ID": "10",
   "Shape_Area": "571.475635931",
   "Dist_No": "1",
   "Shape_Leng": "107.387143989",
   "Block_Numb": "21",
   "OBJECTID": "55"
 }
}
```

The JSON output can then be embedded into web applications as we do in the Web Mapping Assignments


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



### Project 2.2 - Query SQL Server Database with ArcPy

Assignment two requires the programmers to query the sql server database using attribute values of the spatial data

#### Step 1

This team will write ArcPy to query SQL Server. The program should have three parameters which can be easily changed:

1. Parcel
2. Block
3. District

The output should be similar to the following:

Property Type: <value of type>
Property Usage:<value of usage>


[ESRI ArcPy SQL Reference](http://resources.arcgis.com/en/help/main/10.2/index.html#//018z0000007z000000)

#### Step 2

Loop through the shapefile and query the database with the attribute information

For each feature in the parcel shapefile, use the code you developed in step 1 to query the database with parameters from each record in the shapefile


```python
  # change this line to point to your db connection
  sde_conn = arcpy.ArcSDESQLExecute(r"C:/DeRiggiComputer/ArcCatalog/Connection to DAIL13077.sde")
  
  # the sql query
  sql = "select PropertyID, District from IFMSDB.DBO.Property where District = {0} and Block = {1} and ParcelNo = {2}".format(1, 226, 4)          
  
  # the response
  sde_return = sde_conn.execute(sql)
  
```


## 3 Web Maping Assignments


### Project 3.1 - Making simple web maps with our data

In the web mapping assignments we use the json and/or csv files we created with arcpy to build some web based maps with
free open source tools like leaflet js

We will look at a simple case in which make a web map with a place mark
```JavaScript
var map = L.mapbox.map('map',  'examples.map-9ijuk24y' ,{  center: [36.7046, 67.1495], zoom:13, scrollWheelZoom:false});

 var myIcon = L.icon({
  iconUrl: 'images/marker-icon.png',
});

var marker = L.marker(36, 67], {icon: myIcon}).addTo(map);
```

[1) JSON Points on a Map](https://docs.google.com/document/d/1XyVzYlqORZo7VEWlZOtqHNkyyKV1jiKAUseluYVKvW8/edit?usp=sharing)

```JavaScript
// a tiny json object!

{"centroid":[67.11519357832525,36.70581137062923]}
```

### Project 3.2 - Creating a CSV from a Shapefile and Displaying it on Geojson.IO

The second task introduces a site called geojson.io which makes it easy to make a web map from common spatial data
formats. Students modify their scripts to produce CSV files and then simply drag them onto the geojson.io page

[2) Creating CSV files and GeoJson.IO](https://docs.google.com/document/d/1n1tYgcQBd8I7Uxw94ChTBsWeGmwOZ8C7J5av8mxQ7aw/edit?usp=sharing)

