"""
DEMClass
Class to read input data from DEM models and convert to GeoHexMesher inputs
"""

import numpy as np
import os
import sys

class DEMClass:
    ## DEMClass.
    # Class to read input data from DEM Model and convert to GeoHexMesher inputs
    def __init__(self):
        ## The constructor.
        #  @var STLMesh Attribute to store the Lat and Long
        self.STLMesh = np.array([])

    def GetMaterialProperty(self,Inp,OutType=None):
        ## Get the material model
        # @param Inp the input (InputClass) object
        # #param OutType 0 if only save h5, 1 only return, 2 save and return

        if OutType is None:
            Outtype = 2

        InpDir = Inp.WorkDir
        MatType = Inp.PropertyModel
        lim = Inp.Lim
        depth = Inp.Depth #in meters
        depth = depth/1000 #in km

        path = InpDir+os.path.sep+"Material"
        if not os.path.exists(path):
            os.makedirs(path)

        if MatType == "PREM":
            path = path+os.path.sep+"PREM"
            if not os.path.exists(path):
                os.makedirs(path)
            # Load PREM into a DataFrame
            import rockhound as rh
            prem = rh.fetch_prem()
            # filter the depth
            df = prem.loc[prem['depth'] <= depth ]
            l = np.zeros((df.depth.size,4))
            for i in range(0,df.depth.size):
                l[i,0] = lim[0]
                l[i,1] = lim[1]
                l[i,2] = lim[2]
                l[i,3] = lim[3]
            #print(l.shape)
            df['LonMin'] = l[:,0]
            df['LonMax'] = l[:,1]
            df['LatMin'] = l[:,2]
            df['LatMax'] = l[:,3]
            #print(df)
            if OutType == 0:
                # Save the DataFrame in HDF5 format
                h5filename = path+os.path.sep+"Material.h5"
                df.to_hdf(h5filename, key='material', mode='w')
            elif OutType == 1:
                return df
            elif OutType == 2:
                h5filename = path+os.path.sep+"Material.h5"
                print(h5filename)
                df.to_hdf(h5filename, key='material', mode= 'w')
                return df
        else:
            print("This material model is not supported by GeoHexMesher")
            sys.exit(1)

    def GetDEMModel(self,Inp,OutType):
        ## Get the DEM model
        # @param Inp the input (InputClass) object
        # #param OutType 0 if only save h5, 1 only return, 2 save and return

        if OutType is None:
            Outtype = 2
        
        InpDir = Inp.WorkDir
        DEMModel = Inp.DEMModel
        lim = Inp.Lim

        path = InpDir+os.path.sep+"DEM"
        
        if DEMModel == "GEBCO":
            path = path+os.path.sep+"GEBCO"
            filepath = path+os.path.sep+"GEBCO_2022_sub_ice_topo.nc"
            #print(filepath)
            if not os.path.isfile(filepath):
                import requests, zipfile, io
                print("This operation can take several hours")
                zipurl = 'https://www.bodc.ac.uk/data/open_download/gebco/gebco_2022_sub_ice_topo/zip/'
                r = requests.get(zipurl)
                z = zipfile.ZipFile(io.BytesIO(r.content))
                z.extractall(path)
            else:
                #do nothing
                print("The files has been found in your computer")

            import xarray as xr
            ds = xr.open_dataset(filepath)

            # Set the limits of the plot
            minlon, maxlon, minlat, maxlat = lim[0], lim[1], lim[2], lim[3]
            subset = ds.sel(lon=slice(minlon,maxlon))
            subset = subset.sel(lat=slice(minlat, maxlat))

            # Extract the relevant data variables
            lon = subset.lon.values
            lat = subset.lat.values
            depth = subset.elevation.values
            
            # Create the plot
            import matplotlib.pyplot as plt
            # Mask out the negative values
            bathymetry_masked = np.ma.masked_less_equal(depth, 0)

            # Plot the masked bathymetry data
            plt.imshow(bathymetry_masked, cmap='viridis', extent=[np.min(lon), np.max(lon), np.min(lat), np.max(lat)], origin='lower')
            plt.colorbar()
            plt.show()


            '''
            fig, ax = plt.subplots(figsize=(8,8))
            im = ax.imshow(depth, extent=(lon.min(), lon.max(), lat.min(), lat.max()), cmap='coolwarm')
            cbar = plt.colorbar(im, ax=ax, shrink=0.7)
            cbar.set_label('Depth (m)')
            ax.set_xlabel('Longitude')
            ax.set_ylabel('Latitude')
            ax.set_title('GEBCO Bathymetry')
            plt.show()
            '''
        elif DEMModel == "ETOPO1":
            pass
        elif DEMModel == "ETOPO2":
            pass
        elif DEMModel == "GMSTAR":
            pass
        elif DEMModel == "AW3D":
            pass    #https://www.aw3d.jp/en/
        else:
            print("This DEM model is not supported by GeoHexMesher")
            sys.exit(2)
        
        import pandas as pd
        outLat = pd.DataFrame({'lat':lat})
        outLon = pd.DataFrame({'lon':lon})
        outZ   = pd.DataFrame({'z':depth.flatten()})
        #vtkName = path+os.path.sep+"DEMModel.vtk"
        #self.SaveVTK(lat,lon,depth,vtkName)
        #stlName = path+os.path.sep+"DEMModel.stl"
        #self.SaveSTL(lat,lon,depth,stlName)
       # print(df)
        if OutType == 0:
            # Save the DataFrame in HDF5 format
            h5filename = path+os.path.sep+"DEM.h5"
            outLat.to_hdf(h5filename, key='lat', mode='w')
            outLon.to_hdf(h5filename, key='lon')
            outZ.to_hdf  (h5filename, key='z'  )
        elif OutType == 1:
            return outLat, outLon, outZ
        elif OutType == 2:
            h5filename = path+os.path.sep+"DEM.h5"
            outLat.to_hdf(h5filename, key='lat', mode='w')
            outLon.to_hdf(h5filename, key='lon')
            outZ.to_hdf  (h5filename, key='z'  )
            return outLat, outLon, outZ

    def GetCoastLines(self,Inp,OutType):
        ## Get the coastline
        # @param Inp the input (InputClass) object
        # #param OutType 0 if only save h5, 1 only return, 2 save and return
        import os
        import numpy as np
        import pandas as pd

        if OutType is None:
            Outtype = 2
        
        InpDir = Inp.WorkDir
        DEMModel = Inp.DEMModel
        lim = Inp.Lim

        path = InpDir+os.path.sep+"Coastline"
        if not os.path.exists(path):
            os.makedirs(path)

        import cartopy.crs as ccrs
        import cartopy.feature as cfeature
        import pandas as pd
        from shapely.geometry import LineString

        # Define the coastline feature
        coastlines = cfeature.NaturalEarthFeature(category='physical', name='coastline', scale='10m',edgecolor='black', facecolor='none')

        # Define the projection
        proj = ccrs.PlateCarree()

        # Create a figure and axis
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(subplot_kw=dict(projection=proj))

        # Add the coastlines to the axis
        ax.add_feature(coastlines)

        # Extract the coordinates
        coords = []
        for geometry in coastlines.geometries():
            if isinstance(geometry, LineString):
                coords.extend(list(geometry.coords))

        # Store the coordinates in a Pandas dataframe
        df = pd.DataFrame(coords, columns=['lon', 'lat'])

        # Filter between latitudes and longitudes 
        lat_min, lat_max = lim[2], lim[3]
        lon_min, lon_max = lim[0], lim[1]

        df_filtered = df[(df['lat'] >= lat_min) & (df['lat'] <= lat_max) & (df['lon'] >= lon_min) & (df['lon'] <= lon_max)]

        h5filename = path+os.path.sep+"Coastlines.h5"
        df_filtered.to_hdf(h5filename,key='lat',mode='w')
        df_filtered.to_hdf(h5filename,key='lon')
	    
        return df_filtered

    def MergeInfo(self,stl):
        ## evaluate the minimisation of the energy
        #  @param stl something.
	    return

    def SaveVTK(self,x,y,z,vtkName):
        ## Save a vtk binary file
        #  @param vtkName stl filename.
        #  @param x lat 
        #  @param y lon
        #  @param z depth
        import pyvista as pv
        import numpy as np
        import matplotlib as plt
        import matplotlib.pyplot as plt
        '''
        # Create the plot
        fig, ax = plt.subplots(figsize=(8,8))
        im = ax.imshow(z, extent=(x.min(), x.max(), y.min(), y.max()), cmap='coolwarm')
        cbar = plt.colorbar(im, ax=ax, shrink=0.7)
        cbar.set_label('Depth (m)')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_title('GEBCO Bathymetry')

        plt.show()
        '''
        # Create a surface mesh
        X, Y = np.meshgrid(x,y)
        #print(x.shape)
        #print(y.shape)
        #print(z.shape)
        #print(X.shape)
        #print(Y.shape)
        mesh = pv.StructuredGrid(X, Y, z)
        plotter = pv.Plotter()
        plotter.add_mesh(mesh, color="white")
        plotter.show()

        # Save the mesh as an STL file
        mesh.save(vtkName)
        return mesh

    def SaveSTL(self,x,y,z,stlName):
        ## evaluate the triangulation and save a stl binary file
        #  @param stlName stl filename.
        #  @param x 
        #  @param y
        #  @param z
        import numpy as np
        points = np.zeros([len(x)*len(y),2])
        zz = np.zeros([len(x)*len(y)])
        #print(len(x))
        #print(len(y))
        #print(points.shape)
        #print(z.shape)
        count = 0
        for i in range(0,len(x)):
            for j in range(0,len(y)):
                points[count,:] = [x[i],y[j]] 
                zz[count] = z[i,j] 
                count = count + 1
        #points = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
        #z = np.sin(np.sqrt(x**2 + y**2))
        #print(count-1)
        z = zz
        from scipy.spatial import Delaunay
        points = np.column_stack([points[:,0], points[:,1], z])
        tri = Delaunay(points[:,:2])
        #aux = tri.vertices.shape
        #print(aux)
        #print(tri)
        #print(tri.simplices)
        from stl import mesh
        faces = tri.simplices
        mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                mesh.vectors[i][j] = points[f[j],:]

        # Write the mesh to file
        mesh.save(stlName)
        return mesh

        '''
        # Extract the simplices (triangles) from the Delaunay triangulation
        simplices = tri.simplices
       
       # Compute the colors based on z
       # Compute the colors based on z for each vertex of the mesh
        colors = np.zeros_like(points)
        colors[:, 2] = z  # Set the z-component of the color to z
        vmin, vmax = z.min(), z.max()  # Color range

        import matplotlib.pyplot as plt
        #plt.triplot(points[:,0], points[:,1], tri.simplices)
        #plt.plot(points[:,0], points[:,1], 'o')
        #plt.show()

        # Create the 3D mesh
        #import matplotlib.pyplot as plt
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        mesh = Poly3DCollection(points[simplices], facecolors=plt.cm.jet((colors[:, 2] - vmin) / (vmax - vmin)), alpha=0.7)
        ax.add_collection3d(mesh)

        # Set the axis limits
        ax.set_xlim([x.min(), x.max()])
        ax.set_ylim([y.min(), y.max()])
        ax.set_zlim([z.min(), z.max()])
        # Add a colorbar
        scalar_map = plt.cm.ScalarMappable(cmap=plt.cm.jet)
        scalar_map.set_array(colors)
        cbar = plt.colorbar(scalar_map)
        scalar_map.set_clim(vmin=z.min(), vmax=z.max())

        # Plot the mesh
        plt.show()
        '''


        '''
        import numpy as np
        from stl import mesh

        print(x.shape)
        print(y.shape)
        print(z.shape)
        # Create an STL mesh from the x, y, and z data
        vertices = np.zeros((len(x) * len(y), 3))
        #faces = np.zeros((2 * (len(x) - 1) * (len(y) - 1), 3), dtype=np.uint32)
        faces = np.zeros((2*len(x)*len(y),3),dtype=np.uint32)
        for i in range(len(x)):
            for j in range(len(y)):
                idx = i * len(y) + j
                vertices[idx, 0] = x[i]
                vertices[idx, 1] = y[j]
                vertices[idx, 2] = z[i, j]
                if i < len(x) - 1 and j < len(y) - 1:
                    idx1 = i * len(y) + j
                    idx2 = (i + 1) * len(y) + j
                    idx3 = i * len(y) + j + 1
                    idx4 = (i + 1) * len(y) + j + 1
                    faces[2*idx1, :] = [idx1, idx2, idx3]
                    faces[2*idx1+1, :] = [idx2, idx4, idx3]

        # Create an STL object and save to file
        stl_mesh = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
        for i, f in enumerate(faces):
            for j in range(3):
                stl_mesh.vectors[i][j] = vertices[f[j], :]
        stl_mesh.save(stlName)
        return stl_mesh
        '''

    def LoadSTL(self,StlName):
        ## evaluate the minimisation of the energy
        #  @param stl something.
        from stl import mesh

        # Load the STL file
        stl_mesh = mesh.Mesh.from_file('path/to/mesh.stl')

        # Access the vertices and faces of the mesh in vector
        #vertices = stl_mesh.vectors.reshape((-1, 3))
        #faces = stl_mesh.vectors.reshape((-1, 3))
        return stl_mesh
