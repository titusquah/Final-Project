
from sklearn import cluster
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from skimage.measure import label, regionprops


def white_finder(fname,z):
  Img = plt.imread(fname)
  thresh=220;  #cutoff between B & W
  def_center=256
  def_d=427.0
  def_rad=def_d/2-8
  
  core_d=8.75/12
  
  IBinary = (Img[:,:,2] > thresh) #array where true at brightness > threshold
  x=[]
  y=[]
  for i in range(len(IBinary)):
    for j in range(len(IBinary)):
      if IBinary[-i,j]:
        x.append(j)
        y.append(i)
  
  thresh2=150
  circle_binary=(Img[:,:,2] > thresh2)
  label_image = label(circle_binary)
  region_properties = regionprops(label_image, coordinates='rc')
  
  d=[]
  e=[]
  minx=[]
  maxx=[]
  miny=[]
  maxy=[]
  i=0
  for region in region_properties:  #loop through all the discovered objects
      # take regions with large enough areas
      ###########   Only take larger obejects (remove specs)
      ###########   Depending on the resolution of your camera
      ###########   you may need to change this min size on next line
      if region.area >= 100:  
          # draw rectangle around segmented coins
          minr, minc, maxr, maxc = region.bbox  #object's bounding box
          d.append((maxc - minc + maxr - minr)/2) #diameter is avg of width & height
          e.append( region.eccentricity  )#closer to 0 is closer to circle
          minx.append(minc)
          maxx.append(maxc)
          miny.append(minr)
          maxy.append(maxr)
          i+=1  #advance counter
  try:
    argmin=np.argmin(e)
  except:
    return
#  print(min(e))
  if min(e)>0.5:
    center_x=def_center
    center_y=def_center
    diameter=def_d
    rad=def_rad
    
  else:
    center_x=np.mean([minx[argmin],maxx[argmin]])
    center_y=np.mean([miny[argmin],maxy[argmin]])
    diameter=(maxx[argmin]-minx[argmin]+maxy[argmin]-miny[argmin])/2
    rad=diameter/2-5
  
  circle=pd.DataFrame({'x':x,'y':y})
  circle['cent_dist']=np.sqrt((circle['x'].values-center_x)**2+(circle['y'].values-center_y)**2)
  circle=circle[circle['cent_dist']<rad]
  x=circle['x'].values
  y=circle['y'].values
  
  X=[]
  for i in range(len(x)):
    X.append([x[i],y[i]])
  X=np.array(X)
  try:
    db_model = cluster.DBSCAN(eps=3, min_samples=8)
    db_model.fit(X)
    y_pred = db_model.fit_predict(X)
  except:
    return
  
  hi=pd.DataFrame({'x':X[:,0]/diameter*core_d,'y':X[:,1]/diameter*core_d,'y_pred':y_pred})
  
  hi=hi[hi['y_pred']>0]
  
#  plt.figure(figsize=(10,10))
#  plt.scatter(hi['x'],hi['y'], s=1, c=hi['y_pred'], cmap='viridis')
#  #plt.scatter([center_x],[center_y])
#  #plt.imshow(IBinary)
#  plt.show()
  return [hi['x'].values,hi['y'].values,z*np.ones(len(hi))]
      

  


