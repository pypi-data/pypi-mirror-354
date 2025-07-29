# paros_data_grabber

A Python package to securely query Parosbox InfluxDB data using encrypted credentials.

---

## Features

- Loads encrypted InfluxDB credentials bundled inside the package.
- Prompts user for a password to decrypt credentials securely.
- Queries InfluxDB using Flux queries.
- Processes and exports data to CSV, MATLAB `.mat`, or pickle formats.
- Easy to extend and customize.

---

## Installation

Make sure you have Python 3.7+ installed.


```bash
pip install paros-data-grabber==0.1.1.

pip install influxdb-client pandas scipy cryptography pytz  # Install these if not already installed

```
## Example Usage
```python

import os
import numpy as np
from paros_data_grabber import query_influx_data, save_data

# Fetch sensor data
data = query_influx_data(
    start_time="2025-02-25T17:30:00",
    end_time="2025-02-25T18:15:00",
    box_id="parosD",
    sensor_id="142180",
)

# Convert to NumPy arrays if needed
data_arrays = {key: df.values for key, df in data.items()}

# Print shape and a preview of each result
for key, arr in data_arrays.items():
    print(f"Data for {key} has shape {arr.shape}")

for key, df in data.items():
    print(f"First 100 rows for {key}:")
    print(df.head(100))
    print("\n")

# Save to file
save_data(data,  "output.csv")
```