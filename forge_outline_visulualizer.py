
import matplotlib.pyplot as plt
import shapefile
shpFilePath = r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\Roosevelt Hot Springs FORGE Site Outline\FORGE_Outline.shp"
listx=[]
listy=[]
test = shapefile.Reader(shpFilePath)
for sr in test.shapeRecords():
    for xNew,yNew in sr.shape.points:
        listx.append(xNew)
        listy.append(yNew)
plt.plot(listx,listy)
plt.show()