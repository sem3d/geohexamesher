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

    def GetMaterialProperty(self,Inp):
        ## Get the material model
        # @param Inp the input (InputClass) object
        
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
            print(depth)
            df = prem.loc[prem['depth'] <= depth ]
            print(df)
            #save the prem model in the folder

        else:
            print("This material model is not supported by GeoHexMesher")    


        #download the data in the path

    def GetDEMModel(self,lim):
        ## Get the DEM model
        path = InpDir+os.path.sep+"DEM"



        #mesma coisa do de cima

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
