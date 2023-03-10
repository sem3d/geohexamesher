"""
MeshClass
Class to deal with the mesh of GeoHexMesher
"""

import numpy as np
from ElementClass import ElementClass
from NodeClass import NodeClass
from GMTSARClass import GMTSARClass
from InputClass import InputClass
from PolyCubeClass import PolyCubeClass

class MeshClass:
    ## MeshClass.
    # Class to generate the mesh
    def __init__(self):
        ## The constructor.
        #  @var Coords
        #  @var Inputs
        #  @var Elements
        #  @var GTM
        #  @var PolyCube

        self.Coords = np.array([])
        self.Inputs = InputClass()
        self.Elements =  [] # ElementClass()
        self.GTM =  GMTSARClass()
        self.PolyCube = [] #PolyCubeClass()

    def SaveMehsH5(self):
        return None
    
    def BuildMesh(self):
        # Build mesh method. It re

        #1 - get the topo, bathy, coastline info
        self.GTM.GetSurfaces(self.Inputs.Lim)
        #self.GTM.GetTopo(self.Inputs.Lim)
        #self.GTM.GetBathy(self.Inputs.Lim)
        #self.GTM.GetCoastLines(self.Inputs.Lim)
        #self.GTM.MergeInfo
        #debug propose
        self.GTM.SaveSTL('DebugMesh.stl')
        
        #2 build the reference mesh to generate the polycube 
        # it should divide the mesh in semantic areas
        # evaluate the numer of elements
        BB = self.GTM.getBB #get bounding box of the meshes

        #here we should convert the size of element and the the BB in number of elements ineach direction
        nx = 3**6
        ny = 3**6
        nz = [30,10, 5]#the last layer is the transition zone

        #calc the total number of elements
        ntotal = nx*ny*nz[0] #tototo

        print("The mesh has"+ntotal+" elements")
        
        #build the logic to construct the loops here
        #for z
        #for y
        #for x


        #it can/should have more than one closed stl file
        # loop in the closed meshes
        #for imesh in range(1,1):
            





        #return None
    
    def AddPML():
        return None
