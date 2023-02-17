from pygmtsar import SBAS
import matplotlib
import holoviews as hv
from dask.distributed import Client
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import pandas as pd
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

# plot
plt.figure(figsize=(12, 4), dpi=150)
dem = sbas.get_dem()
dem[::4, ::4].plot.imshow(cmap='gray', vmin=0)
sbas.to_dataframe().plot(color='orange', alpha=0.2, ax=plt.gca())
plt.title('Sentinel1 Frame on DEM', fontsize=18)
plt.show()
