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
            df['LatMin'] = l[:,0]
            df['LatMax'] = l[:,1]
            df['LonMin'] = l[:,2]
            df['LonMax'] = l[:,3]
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

            if not os.path.isfile(filepath):
                import requests, zipfile, io
                print("This operation can take several hours")
                zipurl = 'https://www.bodc.ac.uk/data/open_download/gebco/gebco_2022_sub_ice_topo/zip/'
                #r = requests.get(zipurl)
                #z = zipfile.ZipFile(io.BytesIO(r.content))
                #z.extractall(path)
            else:
                #do nothing
                print("The files has been found in your computer")

            import xarray as xr
            ds = xr.open_dataset(filepath)

            # Set the limits of the plot
            minlon, maxlon, minlat, maxlat = lim[2], lim[3], lim[0], lim[1]
            subset = ds.sel(lon=slice(minlon,maxlon))
            subset = subset.sel(lat=slice(minlat, maxlat))

            # Extract the relevant data variables
            lon = subset.lon.values
            lat = subset.lat.values
            depth = subset.elevation.values

        elif DEMModel == "ETOPO1":

        elif DEMModel == "ETOPO2":

        elif DEMModel == "GMSTAR":

        elif DEMModel == "AW3D":
                #https://www.aw3d.jp/en/
        else:
            print("This DEM model is not supported by GeoHexMesher")
            sys.exit(2)
        
       import pandas as pd
       out = pd.DataFrame({'lat':lat,'lon':lon,'z':depth})
       #print(df)
       if OutType == 0:
            # Save the DataFrame in HDF5 format
            h5filename = path+os.path.sep+"DEM.h5"
            out.to_hdf(h5filename, key='DEM', mode='w')
       elif OutType == 1:
            return out
       elif OutType == 2:
            h5filename = path+os.path.sep+"DEM.h5"
            print(h5filename)
            out.to_hdf(h5filename, key='DEM', mode= 'w')
            return out

    def GetSurfaces(self,lim):
        ## Manage the methods to return the final input to polycube
        # @param lim LAT and LON of the region to be meshed

        self.GetTopo(lim)
        self.GetBathy(lim)
        self.GetCoastLine(lim)
        self.MergeInfo(lim)

    def GetTopo(self,stl):
    ## Here it forms the polycube
    #  @param stl something.
	    return

    def GetBathy(self,stl):
    ## here we build the tetmesh and add label to the surfaces
    #  @param stl something.
	    return

    def GetCoastLines(self,stl):
    ## evaluate the minimisation of the energy
    #  @param stl something.
	    return

    def MergeInfo(self,stl):
    ## evaluate the minimisation of the energy
    #  @param stl something.
	    return

    def BuildSTL(self,stl):
    ## compute the stl
    # @param stl
    #it should return N stl meshes
        return

    def SaveSTL(self,stl):
    ## evaluate the minimisation of the energy
    #  @param stl something.
	    return

    def LoadSTL(self,stl):
    ## evaluate the minimisation of the energy
    #  @param stl something.
	    return
