"""
GMTSARClass
Class to read input mesh data from GMTSAR and convert to GeoHexMesher inputs
"""

import numpy as np

class GMTSARClass:
    ## GMTSARClass.
    # Class to read input mesh data from GMTSAR and convert to GeoHexMesher inputs
    def __init__(self):
        ## The constructor.
        #  @var STLMesh Attribute to store the Lat and Long
        self.STLMesh = np.array([])


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
