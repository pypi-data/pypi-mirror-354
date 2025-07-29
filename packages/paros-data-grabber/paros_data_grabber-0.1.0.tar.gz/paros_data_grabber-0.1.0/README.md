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
pip install paros_data_grabber.

pip install influxdb-client pandas scipy cryptography pytz

```
## Example Usage
```python

from paros_data_grabber import query_influx_data, save_data

# Example query
data = query_influx_data(
    start_time="2024-01-01T00:00:00",
    end_time="2024-01-02T00:00:00",
    box_id="parosbox1",
    sensor_id="sensorA",
    bucket="parosbox",
    input_zone="Etc/UTC",
    output_zone="Etc/UTC"
)

# Save results to CSV files
save_data(data, "output.csv")

```