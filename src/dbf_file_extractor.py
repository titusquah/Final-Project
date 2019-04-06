import pandas as pd
#from simpledbf import Dbf5
import shapefile

shpFilePath = r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Utah_FORGE_gravity.shp"

line_dict={}
#df=pd.DataFrame(columns=['x','y'])
test = shapefile.Reader(shpFilePath)
inds=[]
listx=[]
listy=[]
cbga=[]

for ind,sr in enumerate(test.shapeRecords()):
  inds.append(ind)
  cbga.append(test.record(ind)[-2])
#  print(sr.shape.points)
  for xNew,yNew in sr.shape.points:
#    print(xNew)
    listx.append(xNew)
    listy.append(yNew)
    
df=pd.DataFrame({'x':listx,'y':listy,'cbga':cbga})

df.to_csv('gravity_pts.csv')
