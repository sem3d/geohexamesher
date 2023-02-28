from MeshClass import MeshClass
from ElementClass import ElementClass
from NodeClass import NodeClass
from GMTSARClass import GMTSARClass
from InputClass import InputClass
from PolyCubeClass import PolyCubeClass

M = MeshClass()
E = ElementClass()
N = NodeClass()
G = GMTSARClass()
I = InputClass()
P = PolyCubeClass()



print(M)
print(E)
print(N)
print(G)
print(I)
print(P)


I.ReadConfigFile('config.txt')

print('Lim:', I.Lim)
print('Elz:', I.Elz)
print('Elxy:', I.Elxy)
print('ZMax:', I.ZMax)
