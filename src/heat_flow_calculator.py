from sklearn.gaussian_process import GaussianProcessRegressor
import sklearn.gaussian_process.kernels as ker
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools

import fault_visulizer as fv
import forge_polygon_classifier as fpc
import matplotlib
font = {'family' : 'DejaVu Sans',
        'size'   : 16}

matplotlib.rc('font', **font)
#%%Load data
temp_grad_df=pd.read_csv(r"..\..\all_temp_gradient_pts.csv",index_col=0)

therm_cond_df=pd.read_csv(r"..\..\all_thermal_conductivity_pts.csv",index_col=0)

well_loc_df=pd.read_csv(r"../../well_location_from_earth_model.csv",index_col=0)
surf_df=pd.read_csv(r"../../land_surface_vertices.csv")

pt_58_32=pd.read_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\Data\58-32_pts.csv")

cutoff=4000
y_ub=4.3333333333e6
y_lb=4.15e6
num_pts=2000


temp_grad_df=temp_grad_df[(temp_grad_df['depth']<cutoff)&(temp_grad_df['y']<y_ub)&(temp_grad_df['y']>y_lb)]
T_med=temp_grad_df['temp_gradient'].median()
T_UQ=temp_grad_df['temp_gradient'].quantile([0.75])[0.75]
T_LQ=temp_grad_df['temp_gradient'].quantile([0.25])[0.25]
T_IQR=(T_UQ-T_LQ)*1.5
#temp_grad_df=temp_grad_df[(temp_grad_df['temp_gradient']<T_UQ+T_IQR)&(temp_grad_df['temp_gradient']>T_LQ-T_IQR)]

therm_cond_df=therm_cond_df[(therm_cond_df['depth']<cutoff)&(therm_cond_df['y']<y_ub)&(therm_cond_df['y']>y_lb)]


#x=np.array([well_loc_df['x'].values, well_loc_df['y'].values,-well_loc_df['depth (m)'].values]).T
#xtest,ytest,ztest=np.meshgrid(np.random.randint(min(temp_grad_df['x']),max(temp_grad_df['x']),num_pts),
#              np.random.randint(min(temp_grad_df['y']),max(temp_grad_df['y']),num_pts),
#              np.random.randint(min(temp_grad_df['depth']),max(temp_grad_df['depth']),num_pts))
#x = np.column_stack([xtest.flatten(), ytest.flatten(), ztest.flatten()])

x = np.column_stack([np.random.randint(min(surf_df['x']),max(surf_df['x']),num_pts),
              np.random.randint(min(surf_df['y']),max(surf_df['y']),num_pts),
              np.random.randint(min(well_loc_df['depth (m)']),max(well_loc_df['depth (m)']),num_pts)])

#x = np.column_stack([np.random.randint(min(therm_cond_df['x']),max(therm_cond_df['x']),num_pts),
#              np.random.randint(min(therm_cond_df['y']),max(therm_cond_df['y']),num_pts),
#              np.random.randint(min(therm_cond_df['depth']),max(therm_cond_df['depth']),num_pts)])

temp_X = np.array([temp_grad_df['x'].values, temp_grad_df['y'].values,temp_grad_df['depth'].values]).T

temp_y=temp_grad_df['temp_gradient'].values

therm_X = np.array([therm_cond_df['x'].values, therm_cond_df['y'].values,therm_cond_df['depth'].values]).T
therm_y=therm_cond_df['thermal_conductivity'].values

bounds=np.array([[min(surf_df['x']),min(surf_df['y'])],
         [min(surf_df['x']),max(surf_df['y'])],
         [max(surf_df['x']),max(surf_df['y'])],
         [max(surf_df['x']),min(surf_df['y'])],
         [min(surf_df['x']),min(surf_df['y'])]])
#%% KRIGING
#
kernel =   ker.ConstantKernel()+ker.RBF()+ker.RationalQuadratic()

temp_gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9,normalize_y=True)
temp_gp.fit(temp_X, temp_y)

print(temp_gp.score(temp_X, temp_y))

therm_gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=9,normalize_y=True)
therm_gp.fit(therm_X, therm_y)

print(therm_gp.score(therm_X, therm_y))
#%%
z=0
x = np.linspace(min(surf_df['x']),max(surf_df['x']),200)
y = np.linspace(min(surf_df['y']),max(surf_df['y']),200)
X, Y = np.meshgrid(x, y)
x_flatten=X.flatten()
y_flatten=Y.flatten()
Xs=np.column_stack([x_flatten,y_flatten,z*np.ones(len(x_flatten))])
temp_50,sigma=temp_gp.predict(Xs, return_std=True)
therm_50,sigma=therm_gp.predict(Xs, return_std=True)
heatflow_50=temp_50*therm_50
heatflow_50=np.reshape(heatflow_50,(200,200))
#%%
fig, ax = plt.subplots()
ax.plot(fv.x, fv.y, 'red')
CS = ax.contourf(X, Y, heatflow_50)
#ax.clabel(CS, inline=1, fontsize=10)
#ax.set_title('Estimated Heatflow Contour plot  at surface')
plt.show()
#%%Max searcher
pt_search=100

max_pts=[]
max_locs=[]
final_inds=[]
for j in range(1000):
  if j%100==0:
    print(j)
  init_guess=np.array([np.random.randint(surf_df['x'].min(),max(surf_df['x'])),
              np.random.randint(surf_df['y'].min(),max(surf_df['y'])),
              np.random.randint(min(well_loc_df['depth (m)']),max(well_loc_df['depth (m)']))])
  pt_groups=[]
  for i in range(len(init_guess)):
    pt_groups.append(init_guess[i]+pt_search*np.arange(-1,2))
  pts_around=np.array([p for p in itertools.product(*pt_groups)])
  hm_old=-11
  hm_new=0
  ind=0
  while hm_new-hm_old>1e-5 and ind<10000:
    
    hm_old=hm_new
    temp_pred, temp_sigma = temp_gp.predict(pts_around, return_std=True)
    therm_pred, sigma_sigma = therm_gp.predict(pts_around, return_std=True)
    heat_flow_pred=temp_pred*therm_pred
    argmax=np.argmax(heat_flow_pred)
    
    hm_new=max(heat_flow_pred)
    init_guess=pts_around[argmax]
    pt_groups=[]
    for i in range(len(init_guess)):
      pt_groups.append(init_guess[i]+pt_search*np.arange(-1,2))
    pts_around=np.array([p for p in itertools.product(*pt_groups)])
    ind+=1
  
  
  max_pts.append(hm_new)
  max_locs.append(init_guess)
  final_inds.append(ind)
  
#%% format data
max_pts=np.array(max_pts)
max_locs=np.array(max_locs)
pts_df=pd.DataFrame({'x':max_locs[:,0],'y':max_locs[:,1],'z':max_locs[:,2],'heatflow':max_pts,'ind':final_inds})  
pts_df=pts_df.sort_values(by=['heatflow'],ascending=False)
pts_df=pts_df[(pts_df['x']>min(surf_df['x']))&(pts_df['x']<max(surf_df['x']))&\
               (pts_df['y']>min(surf_df['y']))&(pts_df['y']<max(surf_df['y']))]
pts_df=pts_df[(pts_df['ind']!=2)]
#%%Plot
#plt.close('all')
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot3D(bounds[:,0],bounds[:,1],0,'red',alpha=1)
ax.plot3D(fv.x, fv.y, 0, 'red')
ax.plot3D(fv.x_bot, fv.y_bot, -max(temp_grad_df['depth']), 'red')
for i in range(len(fv.x)):
  ax.plot3D([fv.x[i],fv.x_bot[i]], [fv.y[i],fv.y_bot[i]], [0,-max(temp_grad_df['depth'])], 'red')
##
#pts=ax.scatter3D(x[:,0],x[:,1],-x[:,2],c=(temp_pred),cmap='inferno',alpha=1)
#fig.colorbar(pts, shrink=0.5, aspect=5)
##ax.scatter3D(temp_X[:,0],temp_X[:,1],temp_X[:,2],c=temp_y,cmap='inferno',alpha=1)
##for i, val in enumerate(temp_y):
##    ax.text(temp_X[i,0],temp_X[i,1],temp_X[i,2],'hi')
#
##ax.scatter3D(x[:,0],x[:,1],x[:,2],c=therm_pred,cmap='inferno',alpha=1)
##ax.scatter3D(therm_X[:,0],therm_X[:,1],therm_X[:,2],c=therm_y,cmap='inferno',alpha=1)
##for i, val in enumerate(therm_y):
##    ax.text(therm_X[i,0],therm_X[i,1],therm_X[i,2],'hi')
#
ax.plot3D(pt_58_32['x'],pt_58_32['y'],pt_58_32['z']-max(pt_58_32['z']))
pts=ax.scatter3D(pts_df['x'],pts_df['y'],-pts_df['z'],c=(pts_df['heatflow']),cmap='inferno',alpha=1)
fig.colorbar(pts, shrink=0.5, aspect=5)
plt.show()
#%% min searcher
pt_search=100

min_pts=[]
min_locs=[]
final_inds=[]
for j in range(1000):
  if j%100==0:
    print(j)
  init_guess=np.array([np.random.randint(surf_df['x'].min(),max(surf_df['x'])),
              np.random.randint(surf_df['y'].min(),max(surf_df['y'])),
              np.random.randint(min(well_loc_df['depth (m)']),max(well_loc_df['depth (m)']))])
  pt_groups=[]
  for i in range(len(init_guess)):
    pt_groups.append(init_guess[i]+pt_search*np.arange(-1,2))
  pts_around=np.array([p for p in itertools.product(*pt_groups)])
  hm_old=100000
  hm_new=10000
  ind=0
  while hm_old-hm_new>1e-5 and ind<10000:
    
    hm_old=hm_new
    temp_pred, temp_sigma = temp_gp.predict(pts_around, return_std=True)
    therm_pred, sigma_sigma = therm_gp.predict(pts_around, return_std=True)
    heat_flow_pred=temp_pred*therm_pred
    argmin=np.argmin(heat_flow_pred)
    
    hm_new=min(heat_flow_pred)
    init_guess=pts_around[argmin]
    pt_groups=[]
    for i in range(len(init_guess)):
      pt_groups.append(init_guess[i]+pt_search*np.arange(-1,2))
    pts_around=np.array([p for p in itertools.product(*pt_groups)])
    ind+=1
  
  
  min_pts.append(hm_new)
  min_locs.append(init_guess)
  final_inds.append(ind)
  
#%% format data
min_pts=np.array(min_pts)
min_locs=np.array(min_locs)
pts_df=pd.DataFrame({'x':min_locs[:,0],'y':min_locs[:,1],'z':min_locs[:,2],'heatflow':min_pts,'ind':final_inds})  
pts_df=pts_df.sort_values(by=['heatflow'],ascending=False)
pts_df=pts_df[(pts_df['x']>min(surf_df['x']))&(pts_df['x']<max(surf_df['x']))&\
               (pts_df['y']>min(surf_df['y']))&(pts_df['y']<max(surf_df['y']))]
pts_df=pts_df[(pts_df['ind']!=2)]
#%%Plot
#plt.close('all')
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot3D(bounds[:,0],bounds[:,1],0,'red',alpha=1)
ax.plot3D(fv.x, fv.y, 0, 'red')
ax.plot3D(fv.x_bot, fv.y_bot, -max(temp_grad_df['depth']), 'red')
for i in range(len(fv.x)):
  ax.plot3D([fv.x[i],fv.x_bot[i]], [fv.y[i],fv.y_bot[i]], [0,-max(temp_grad_df['depth'])], 'red')
##
#pts=ax.scatter3D(x[:,0],x[:,1],-x[:,2],c=(temp_pred),cmap='inferno',alpha=1)
#fig.colorbar(pts, shrink=0.5, aspect=5)
##ax.scatter3D(temp_X[:,0],temp_X[:,1],temp_X[:,2],c=temp_y,cmap='inferno',alpha=1)
##for i, val in enumerate(temp_y):
##    ax.text(temp_X[i,0],temp_X[i,1],temp_X[i,2],'hi')
#
##ax.scatter3D(x[:,0],x[:,1],x[:,2],c=therm_pred,cmap='inferno',alpha=1)
##ax.scatter3D(therm_X[:,0],therm_X[:,1],therm_X[:,2],c=therm_y,cmap='inferno',alpha=1)
##for i, val in enumerate(therm_y):
##    ax.text(therm_X[i,0],therm_X[i,1],therm_X[i,2],'hi')
#
ax.plot3D(pt_58_32['x'],pt_58_32['y'],pt_58_32['z']-max(pt_58_32['z']))
pts=ax.scatter3D(pts_df['x'],pts_df['y'],-pts_df['z'],c=(pts_df['heatflow']),cmap='inferno',alpha=1)
fig.colorbar(pts, shrink=0.5, aspect=5)
plt.show()
#%%Save data
#pts_df.to_csv(r"C:\Users\tq220\Documents\Tits things\2018-2019\Data Science\Final-project-data\max_heat_flow_in_extent.csv")
#%%forge footprint pt load
forge_pts=pd.read_csv(r"..\..\forge_classifier.csv")
forge_pts=forge_pts[forge_pts['in']==1]
forge_pts=forge_pts.reset_index()
#%%max searcher within footprint
pt_search=10

max_pts=[]
max_locs=[]
final_inds=[]
for j in range(1000):
  if j%100==0:
    print(j)
  rand_index=np.random.randint(0,len(forge_pts)-1)
  
  init_guess=np.array([forge_pts['x'][rand_index],
              forge_pts['y'][rand_index],
              np.random.randint(min(well_loc_df['depth (m)']),max(well_loc_df['depth (m)']))])
  pt_groups=[]
  for i in range(len(init_guess)):
    pt_groups.append(init_guess[i]+pt_search*np.arange(-1,2))
  pts_around=np.array([p for p in itertools.product(*pt_groups)])
  hm_old=-11
  hm_new=0
  ind=0
  while hm_new-hm_old>1e-5 and ind<10000 and fpc.p.contains_points(
      np.array([[init_guess[0],init_guess[1]]]))[0]:
    
    hm_old=hm_new
    temp_pred, temp_sigma = temp_gp.predict(pts_around, return_std=True)
    therm_pred, sigma_sigma = therm_gp.predict(pts_around, return_std=True)
    heat_flow_pred=temp_pred*therm_pred
    argmax=np.argmax(heat_flow_pred)
    
    hm_new=max(heat_flow_pred)
    init_guess=pts_around[argmax]
    pt_groups=[]
    for i in range(len(init_guess)):
      pt_groups.append(init_guess[i]+pt_search*np.arange(-1,2))
    pts_around=np.array([p for p in itertools.product(*pt_groups)])
    ind+=1
#  print(init_guess,ind,hm_new)
  
  max_pts.append(hm_new)
  max_locs.append(init_guess)
  final_inds.append(ind)
#%% format data
max_foot_pts=np.array(max_pts)
max_foot_locs=np.array(max_locs)
pts_foot_df=pd.DataFrame({'x':max_foot_locs[:,0],'y':max_foot_locs[:,1],'z':max_foot_locs[:,2],'heatflow':max_foot_pts,'ind':final_inds})  
pts_foot_df=pts_foot_df.sort_values(by=['heatflow'],ascending=False)
#pts_foot_df=pts_foot_df.iloc[:2]
#pts_df=pts_df[(pts_df['x']>min(surf_df['x']))&(pts_df['x']<max(surf_df['x']))&\
#               (pts_df['y']>min(surf_df['y']))&(pts_df['y']<max(surf_df['y']))]
#pts_foot_df=pts_df[(pts_df['ind']!=2)]
#%%Plot
#plt.close('all')
fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.plot3D(bounds[:,0],bounds[:,1],0,'red',alpha=1)
ax.plot3D(fv.x, fv.y, 0, 'red')
ax.plot3D(fv.x_bot, fv.y_bot, -max(temp_grad_df['depth']), 'red')
for i in range(len(fv.x)):
  ax.plot3D([fv.x[i],fv.x_bot[i]], [fv.y[i],fv.y_bot[i]], [0,-max(temp_grad_df['depth'])], 'red')
##
#pts=ax.scatter3D(x[:,0],x[:,1],-x[:,2],c=(temp_pred),cmap='inferno',alpha=1)
#fig.colorbar(pts, shrink=0.5, aspect=5)
##ax.scatter3D(temp_X[:,0],temp_X[:,1],temp_X[:,2],c=temp_y,cmap='inferno',alpha=1)
##for i, val in enumerate(temp_y):
##    ax.text(temp_X[i,0],temp_X[i,1],temp_X[i,2],'hi')
#
##ax.scatter3D(x[:,0],x[:,1],x[:,2],c=therm_pred,cmap='inferno',alpha=1)
##ax.scatter3D(therm_X[:,0],therm_X[:,1],therm_X[:,2],c=therm_y,cmap='inferno',alpha=1)
##for i, val in enumerate(therm_y):
##    ax.text(therm_X[i,0],therm_X[i,1],therm_X[i,2],'hi')
ax.plot3D(pt_58_32['x'],pt_58_32['y'],pt_58_32['z']-max(pt_58_32['z']))
pts=ax.scatter3D(pts_foot_df['x'],pts_foot_df['y'],-pts_foot_df['z'],c=(pts_foot_df['heatflow']),cmap='inferno',alpha=1)
fig.colorbar(pts, shrink=0.5, aspect=5)
plt.show()
#%%min searcher within footprint
pt_search=10

min_pts=[]
min_locs=[]
final_inds=[]
for j in range(1000):
  if j%100==0:
    print(j)
  rand_index=np.random.randint(0,len(forge_pts)-1)
  
  init_guess=np.array([forge_pts['x'][rand_index],
              forge_pts['y'][rand_index],
              np.random.randint(min(well_loc_df['depth (m)']),max(well_loc_df['depth (m)']))])
  
  pt_groups=[]
  for i in range(len(init_guess)):
    pt_groups.append(init_guess[i]+pt_search*np.arange(-1,2))
  pts_around=np.array([p for p in itertools.product(*pt_groups)])

  hm_old=100000
  hm_new=10000
  ind=0
  while hm_old-hm_new>1e-5 and ind<10000 and fpc.p.contains_points(
      np.array([[init_guess[0],init_guess[1]]]))[0]:
    
    hm_old=hm_new
    temp_pred, temp_sigma = temp_gp.predict(pts_around, return_std=True)
    therm_pred, sigma_sigma = therm_gp.predict(pts_around, return_std=True)
    heat_flow_pred=temp_pred*therm_pred
    argmin=np.argmin(heat_flow_pred)
    
    hm_new=min(heat_flow_pred)
    init_guess=pts_around[argmin]
    pt_groups=[]
    for i in range(len(init_guess)):
      pt_groups.append(init_guess[i]+pt_search*np.arange(-1,2))
    pts_around=np.array([p for p in itertools.product(*pt_groups)])
    ind+=1
    
#  print(init_guess,ind,hm_new)
  
  min_pts.append(hm_new)
  min_locs.append(init_guess)
  final_inds.append(ind)
#%% format data
min_foot_pts=np.array(min_pts)
min_foot_locs=np.array(min_locs)
min_pts_foot_df=pd.DataFrame({'x':min_foot_locs[:,0],'y':min_foot_locs[:,1],'z':min_foot_locs[:,2],'heatflow':min_foot_pts,'ind':final_inds})  
min_pts_foot_df=min_pts_foot_df.sort_values(by=['heatflow'],ascending=False)
#pts_foot_df=pts_foot_df.iloc[:2]
#pts_df=pts_df[(pts_df['x']>min(surf_df['x']))&(pts_df['x']<max(surf_df['x']))&\
#               (pts_df['y']>min(surf_df['y']))&(pts_df['y']<max(surf_df['y']))]
#pts_foot_df=pts_df[(pts_df['ind']!=2)]
#%%Plot
#plt.close('all')
fig = plt.figure()
ax = fig.gca(projection='3d')
#ax.plot3D(bounds[:,0],bounds[:,1],0,'red',alpha=1)
ax.plot3D(fv.x, fv.y, 0, 'red')
ax.plot3D(fv.x_bot, fv.y_bot, -max(temp_grad_df['depth']), 'red')
for i in range(len(fv.x)):
  ax.plot3D([fv.x[i],fv.x_bot[i]], [fv.y[i],fv.y_bot[i]], [0,-max(temp_grad_df['depth'])], 'red')
##
#pts=ax.scatter3D(x[:,0],x[:,1],-x[:,2],c=(temp_pred),cmap='inferno',alpha=1)
#fig.colorbar(pts, shrink=0.5, aspect=5)
##ax.scatter3D(temp_X[:,0],temp_X[:,1],temp_X[:,2],c=temp_y,cmap='inferno',alpha=1)
##for i, val in enumerate(temp_y):
##    ax.text(temp_X[i,0],temp_X[i,1],temp_X[i,2],'hi')
#
##ax.scatter3D(x[:,0],x[:,1],x[:,2],c=therm_pred,cmap='inferno',alpha=1)
##ax.scatter3D(therm_X[:,0],therm_X[:,1],therm_X[:,2],c=therm_y,cmap='inferno',alpha=1)
##for i, val in enumerate(therm_y):
##    ax.text(therm_X[i,0],therm_X[i,1],therm_X[i,2],'hi')
#
pts=ax.scatter3D(min_pts_foot_df['x'],min_pts_foot_df['y'],-min_pts_foot_df['z'],c=(min_pts_foot_df['heatflow']),cmap='inferno',alpha=1)
fig.colorbar(pts, shrink=0.5, aspect=5)
plt.show()
temp_grad_df.t
#%%#
z=0
x = np.linspace(min(fv.x),max(fv.x),200)
y = np.linspace(min(fv.y),max(fv.y),200)
X, Y = np.meshgrid(x, y)
x_flatten=X.flatten()
y_flatten=Y.flatten()
Xs=np.column_stack([x_flatten,y_flatten,z*np.ones(len(x_flatten))])
temp_50,sigma=temp_gp.predict(Xs, return_std=True)
therm_50,sigma=therm_gp.predict(Xs, return_std=True)
heatflow_50=temp_50*therm_50
hii=pd.DataFrame({'x':x_flatten,'y':y_flatten,'heatflow':heatflow_50})
hii=hii.sort_values(by=['heatflow'],ascending=False)
heatflow_50=np.reshape(heatflow_50,(200,200))

#%%
i=0
deg=25
deg1=20
deg2=40
dist=1000



prod1=np.array([[hii.iloc[i]['x']-dist/2*np.sin((deg)*np.pi/180),
                                hii.iloc[i]['y']-dist/2*np.cos((deg)*np.pi/180)]])

inj=[]
inj.append([hii.iloc[i]['x'],hii.iloc[i]['y']])
inj.append([hii.iloc[i]['x']-dist*np.sin((deg)*np.pi/180),
                                hii.iloc[i]['y']-dist*np.cos((deg)*np.pi/180)])
inj.append([hii.iloc[i]['x']-dist/2*np.sin((deg)*np.pi/180),
                                hii.iloc[i]['y']-dist/2*np.cos((deg)*np.pi/180)])
inj.append([prod1[0][0]+dist/2*np.sin((deg1)*np.pi/180),prod1[0][1]+\
                dist/2*np.cos((deg1)*np.pi/180)])
inj.append([prod1[0][0]-dist/2*np.sin((deg1)*np.pi/180),prod1[0][1]-\
                dist/2*np.cos((deg1)*np.pi/180)])
inj.append([prod1[0][0]+dist/2*np.sin((deg2)*np.pi/180),prod1[0][1]+\
                dist/2*np.cos((deg2)*np.pi/180)])
inj.append([prod1[0][0]-dist/2*np.sin((deg2)*np.pi/180),prod1[0][1]-\
                dist/2*np.cos((deg2)*np.pi/180)])
inj=np.array(inj)

while not fpc.p.contains_points(inj).all():
  i+=1
  
  prod1=np.array([[hii.iloc[i]['x']-dist/2*np.sin((deg)*np.pi/180),
                                hii.iloc[i]['y']-dist/2*np.cos((deg)*np.pi/180)]])

  inj=[]
  inj.append([hii.iloc[i]['x'],hii.iloc[i]['y']])
  inj.append([hii.iloc[i]['x']-dist*np.sin((deg)*np.pi/180),
                                  hii.iloc[i]['y']-dist*np.cos((deg)*np.pi/180)])
  inj.append([hii.iloc[i]['x']-dist/2*np.sin((deg)*np.pi/180),
                                  hii.iloc[i]['y']-dist/2*np.cos((deg)*np.pi/180)])
  inj.append([prod1[0][0]+dist/2*np.sin((deg1)*np.pi/180),prod1[0][1]+\
                  dist/2*np.cos((deg1)*np.pi/180)])
  inj.append([prod1[0][0]-dist/2*np.sin((deg1)*np.pi/180),prod1[0][1]-\
                  dist/2*np.cos((deg1)*np.pi/180)])
  inj.append([prod1[0][0]+dist/2*np.sin((deg2)*np.pi/180),prod1[0][1]+\
                  dist/2*np.cos((deg2)*np.pi/180)])
  inj.append([prod1[0][0]-dist/2*np.sin((deg2)*np.pi/180),prod1[0][1]-\
                  dist/2*np.cos((deg2)*np.pi/180)])
  inj=np.array(inj)

print(hii.iloc[i]['x'],hii.iloc[i]['y'])
meeko=[0,1,3,4,5,6]
wellx=[]
welly=[]
for i in meeko:
  wellx.append(inj[i][0])
  wellx.append(inj[2][0])
  welly.append(inj[i][1])
  welly.append(inj[2][1])
#%%
fig, ax = plt.subplots()
ax.plot(fv.x, fv.y, 'red')
CS = ax.contour(X, Y, heatflow_50,20)
ax.clabel(CS, inline=1, fontsize=16)
ax.plot(wellx,welly,'ko')
ax.plot(wellx,welly,'k')
ax.plot(wellx[0],welly[0],'ro')
ax.plot(wellx[1],welly[1],'bo')
#ax.set_title('Estimated Heatflow Contour plot  around FORGE and proposed well locations')
ax.grid(True)
plt.show()
