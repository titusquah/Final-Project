
import matplotlib.pyplot as plt
import shapefile
import pandas as pd

shpFilePath = r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Mineral_Mtn_lineaments\Mineral_mtns_lineaments.shp"

line_dict={}
df=pd.DataFrame(columns=['x','y'])
test = shapefile.Reader(shpFilePath)
inds=[]
listx=[]
listy=[]
for ind,sr in enumerate(test.shapeRecords()):
  inds.append(ind)
  listx=[]
  listy=[]
#  print(sr.shape.points)
  for xNew,yNew in sr.shape.points:
#    print(xNew)
    listx.append(xNew)
    listy.append(yNew)
  df.loc['{0}'.format(ind)]=[listx,listy]
#  plt.plot(listx,listy)
#  line_dict['line{0}x'.format(ind)]=listx
#  line_dict['line{0}y'.format(ind)]=listy
  
df.to_csv('surface_fractures_group_by_shape.csv')

#plt.scatter(listx,listy,markersize=1)
#plt.show()  