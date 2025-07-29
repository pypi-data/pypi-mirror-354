# SuperMAG Python Client

The SuperMAG Python Client provides programmatic access to magnetometer data and indices from the SuperMAG web services API. It supports data retrieval, station inventory queries, and data manipulation using Python with built-in pandas support.

## Features

- **Inventory Query**: Retrieve lists of SuperMAG stations for a given event.
- **Magnetometer Data**: Fetch vector magnetic field data (NEZ, geographic) for selected stations.
- **Magnetic Indices**: Retrieve SuperMAG indices (SME, SMU, SML, etc.) with support for sunlit/dark/regional variations and solar wind parameters.
- **Flexible Output**: Choose between `pandas.DataFrame` or raw `list` outputs via `FORMAT` parameter.
- **Helper Tools**: Utility functions to extract nested dictionary structures, process CSV exports, and perform unit tests.

## Requirements

- Python 3
- `pandas` (`pip install pandas`)
- `certifi` (required at sites with SSL cert enforcement)

## Example Usage

```python
from supermag_api import *
userid = 'YOUR_SUPERMAG_USER_ID'
start = [2019, 11, 15, 10, 40]

# Get inventory
status, stations = SuperMAGGetInventory(userid, start, 3600)

# Fetch data
status, data = SuperMAGGetData(userid, start, 3600, 'all', 'HBK')

# Fetch indices
status, indices = SuperMAGGetIndices(userid, start, 3600, 'all')

# Access nested components
n_nez = sm_grabme(data, 'N', 'nez')

# Quick test
sm_microtest(4, userid)
