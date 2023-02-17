import utm
from pyproj import Proj, transform
import pyvista as pv
from pygmtsar import SBAS
import matplotlib
import holoviews as hv
from dask.distributed import Client
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import pandas as pd
import pdb
# supress numpy warnings
import warnings
warnings.filterwarnings('ignore')

# show interactive plots if allowed
import hvplot.pandas  # noqa
import hvplot.xarray  # noqa
pd.options.plotting.backend = 'hvplot'
gstiles = hv.Tiles(
    'https://mt1.google.com/vt/lyrs=s&x={X}&y={Y}&z={Z}', name='Google Satellite')
ottiles = hv.Tiles(
    'https://tile.opentopomap.org/{Z}/{X}/{Y}.png', name='Open Topo')

# define Pandas display settings
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# Define Parameters
MASTER = '2015-04-03'
WORKDIR = 'raw_stack'
DATADIR = '/home/kltpk89/Data/Filippo/gmtsar/tests/raw_orig'
DEMFILE = '/home/kltpk89/Data/Filippo/gmtsar/tests/topo/dem.grd'
BASEDAYS = 100
BASEMETERS = 150
DEFOMAX = 0

# Run Local Dask Cluster
# client = Client()

# use DEM from the example
sbas = SBAS(DATADIR, DEMFILE, WORKDIR).set_master(MASTER)
sbas.to_dataframe()


dem = sbas.get_dem()[::20, ::20]



LonVec = dem['lon'].to_numpy()
LatVec = dem['lat'].to_numpy()
LonGrid, LatGrid = np.meshgrid(LonVec, LatVec)
EwGrid, NorthGrid, *_  = utm.from_latlon(LatGrid, LonGrid)

ElevationGrid = dem.to_numpy()

# inProj = Proj(init='epsg:3857')
# outProj = Proj(init='epsg:4326')

zcells = np.array([2500] * 5 + [3500] * 3 + [5000] * 2 + [7500, 10000])
# zcells = np.array([1] * 1)
xx = np.repeat(EwGrid[..., np.newaxis], len(zcells), axis=-1)
yy = np.repeat(NorthGrid[..., np.newaxis], len(zcells), axis=-1)
# pdb.set_trace()
zz = np.repeat(ElevationGrid[..., np.newaxis], len(zcells), axis=-1) - \
    np.cumsum(zcells).reshape((1, 1, -1))


mesh = pv.StructuredGrid(xx, yy, zz)

mesh["Elevation"] = zz.ravel(order="F")
mesh.plot(show_edges=True, lighting=False)