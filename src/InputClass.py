"""
InputClass
Class to read input data to GeoHexMesher
"""

class InputClass:
    ## InputClass.
    # Class to read input data
    def __init__(self):
        ## The constructor.
        #  @var Lim Attribute to store the Lat and Long
        #  @var Elz Attribute vector with ehe size of elements in z, each number corresponding to one layer
        #  @var Elxy Attribute size of the elements in x and y for the most refined layer

        self.Lim = []
        self.Elz = []
        self.Elxy = []
        self.ZMax = []

    def ReadConfigFile(self,filename):
    ## Read input file and assign to obj
    #  @param filename Name of the config file.
        with open(filename, 'r') as f:
            for line in f:
                if not line.startswith('#'):
                    name, value = line.split(':')
                    name = name.strip()
                    value = value.split()
                    
                    if name == 'Lim':
                        self.Lim = [float(x) for x in value]
                    elif name == 'Elz':
                        self.Elz = [float(x) for x in value]
                    elif name == 'Elxy':
                        self.Elxy = [float(x) for x in value]
                    elif name == 'ZMax':
                        self.ZMax = [float(x) for x in value]
        self.validate_values()
    
    def validate_values(self):
        ## Validate the inputs.
        assert len(self.Lim) == 4, f'Error: Lim must have 4 values. Got {len(self.Lim)}'
        assert len(self.Elz) >= 1, f'Error: Elz must have at least 1 value. Got {len(self.Elz)}'
        assert len(self.Elxy) == 2, f'Error: Elxy must have 2 values. Got {len(self.Elxy)}'
        assert len(self.Elz) == len(self.ZMax), f'Error: the number of layers in Z and the size of elements do no have the same size, please check the config file'
    
    def __str__(self):
        ## Replace print method
        print('The Input is:')
        print('Lim:',  self.Lim)
        print('Elz:',  self.Elz)
        print('Elxy:', self.Elxy)
        print('ZMax:', self.ZMax)
        return None
