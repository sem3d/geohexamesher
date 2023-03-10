#from MeshClass import MeshClass
#from ElementClass import ElementClass
#from NodeClass import NodeClass
from DEMClass import DEMClass
from InputClass import InputClass
#from PolyCubeClass import PolyCubeClass

#M = MeshClass()
#E = ElementClass()
#N = NodeClass()
D = DEMClass()
I = InputClass()
#P = PolyCubeClass()



#print(M)
#print(E)
#print(N)
#print(G)
#print(I)
#print(P)


I.ReadConfigFile('config.txt')

print(I)
D.GetMaterialProperty(I,2)
D.GetDEMModel(I,2)
D.GetCoastLines(I,2)
