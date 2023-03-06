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
        self.PropertyModel = ''
        self.DEMModel = ''
        self.AddWater = 0        
        self.MaxFrequency = -1
        self.NelPerWavelength = -1
        self.Depth = -1
        self.WorkDir = ''

    def ReadConfigFile(self,filename):
    ## Read input file and assign to obj
    #  @param filename Name of the config file.
        with open(filename, 'r') as f:
            for line in f:
                if not line.startswith('#'):
                    line = line.split('#')[0].strip()
                    name, value = line.split(':')
                    name = name.strip()
                    value = value.split()
                    
                    if name == 'Lim':
                        self.Lim = [float(x) for x in value]
                    elif name == 'PropertyModel':
                        self.PropertyModel  = str(value[0])
                    elif name == 'DEMModel':
                        self.DEMModel = str(value[0])
                    elif name == 'AddWater':
                        if int(value[0]) == 0:
                            self.AddWater = False
                        else:
                            self.AddWater = True
                    elif name == 'MaxFrequency':
                        self.MaxFrequency = float(value[0])
                    elif name == 'NelPerWavelength':
                        self.NelPerWavelength = int(value[0])
                    elif name == 'Depth':
                        self.Depth = float(value[0])
                    elif name == 'WorkDir':
                        self.WorkDir = str(value[0])

        self.validate_values()
    
    #TODO: add the validations
    def validate_values(self):
        ## Validate the inputs.
        assert len(self.Lim) == 4, f'Error: Lim must have 4 values. Got {len(self.Lim)}'

    
    def __str__(self):
        ## Replace print method
        return (f"Lim: {self.Lim}\n"
                f"PropertyModel: {self.PropertyModel}\n"
                f"DEMModel: {self.DEMModel}\n"
                f"AddWater: {self.AddWater}\n"
                f"MaxFrequency: {self.MaxFrequency}\n"
                f"NelPerWavelength: {self.NelPerWavelength}\n"
                f"Depth: {self.Depth}\n"
                f"WorkDir: {self.WorkDir}")
