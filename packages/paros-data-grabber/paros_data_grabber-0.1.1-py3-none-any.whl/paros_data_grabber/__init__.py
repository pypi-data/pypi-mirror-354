import influxdb_client
import pickle
import os
import pytz
import datetime
from scipy.io import savemat
import pandas as pd
import getpass
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import importlib.resources

def load_encrypted_creds_from_package():
    # Load encrypted creds file from package resources
    with importlib.resources.open_binary('paros_data_grabber.creds', 'influx-creds.enc') as f:
        return f.read()

def decrypt_creds(password, enc_data_bytes):
    data = enc_data_bytes

    salt = data[:16]
    nonce = data[16:28]
    encrypted = data[28:]

    kdf = Scrypt(salt=salt, length=32, n=2**14, r=8, p=1)
    key = kdf.derive(password.encode())

    aesgcm = AESGCM(key)
    try:
        decrypted = aesgcm.decrypt(nonce, encrypted, None)
        creds_dict = pickle.loads(decrypted)
        return creds_dict
    except Exception as e:
        raise ValueError("Incorrect password or corrupted credentials file.") from e

def load_influx_client(password, enc_pickle_path=None):
    if enc_pickle_path is None:
        # Use bundled encrypted creds
        enc_data_bytes = load_encrypted_creds_from_package()
    else:
        with open(enc_pickle_path, "rb") as f:
            enc_data_bytes = f.read()
    influx_dict = decrypt_creds(password, enc_data_bytes)
    client = influxdb_client.InfluxDBClient(
        url=influx_dict["idb_url"],
        token=influx_dict["idb_token"],
        org=influx_dict["idb_org"],
        timeout=100_000_000
    )
    return client, client.query_api()

def process_influx_df(df, output_tz):
    cur_box = df["_measurement"].iloc[0]
    cur_id = df["id"].iloc[0]
    id_str = f"{cur_box}_{cur_id}"

    out_df = df.drop(columns=["result", "table", "_measurement", "id"], errors='ignore')
    out_df.drop(columns=[col for col in ["baro_time", "err"] if col in out_df], inplace=True, errors='ignore')
    out_df.rename(columns={'_time': 'time'}, inplace=True)
    out_df["time"] = out_df["time"].dt.tz_convert(output_tz).dt.tz_localize(None)
    out_df["time"] = (out_df["time"] - pd.Timestamp("1970-01-01")) / pd.Timedelta('1s')

    return id_str, out_df

def create_flux_filters(col_name, in_str):
    if not in_str:
        return ""
    in_list = in_str.split(',') if ',' in in_str else [in_str]
    filter_list = [f'r["{col_name}"] == "{i}"' for i in in_list]
    return f'|> filter(fn: (r) => {" or ".join(filter_list)})' if filter_list else ""

def query_influx_data(
    start_time,
    end_time,
    creds=None,        # None means use bundled creds
    password=None,
    box_id=None,
    sensor_id=None,
    bucket="parosbox",
    input_zone="Etc/UTC",
    output_zone="Etc/UTC"
):
    input_tz = pytz.timezone(input_zone)
    output_tz = pytz.timezone(output_zone)

    # Convert start/end to UTC-naive datetime
    start_time = input_tz.localize(datetime.datetime.fromisoformat(start_time))
    end_time = input_tz.localize(datetime.datetime.fromisoformat(end_time))

    start_time_utc = start_time.astimezone(datetime.timezone.utc).replace(tzinfo=None)
    end_time_utc = end_time.astimezone(datetime.timezone.utc).replace(tzinfo=None)

    # Build Flux query
    box_filters = create_flux_filters("_measurement", box_id)
    sensor_filters = create_flux_filters("id", sensor_id)

    query = f'''from(bucket: "{bucket}")
        |> range(start: {start_time_utc.isoformat()}Z, stop: {end_time_utc.isoformat()}Z)'''
    if box_filters:
        query += f'\n\t{box_filters}'
    if sensor_filters:
        query += f'\n\t{sensor_filters}'
    query += '''
        |> drop(columns: ["_start", "_stop"])
        |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")'''

    # Prompt if password wasn't passed
    if password is None:
        password = getpass.getpass("Enter password to decrypt InfluxDB credentials: ")

    # Load client using encrypted credentials (bundled or user-provided)
    client, query_api = load_influx_client(password, enc_pickle_path=creds)

    # Run query
    result = query_api.query_data_frame(query=query)

    # Normalize to list of DataFrames
    dfs = []
    if isinstance(result, list):
        for r in result:
            dfs.extend([r for _, r in r.groupby("table")])
    else:
        dfs.append(result)

    # Process each dataframe
    out_df = {}
    for df in dfs:
        id_str, proc_df = process_influx_df(df, output_tz)
        out_df[id_str] = proc_df

    return out_df

def save_data(out_df, output_file):
    name, ext = os.path.splitext(output_file)
    if ext == ".csv":
        for key, df in out_df.items():
            out_path = f"{name}_{key}.csv"
            df.to_csv(out_path, index=False, header=False)
            print(f"Saved: {out_path}")
    elif ext == ".mat":
        mat_dict = {key: df.values for key, df in out_df.items()}
        savemat(output_file, mat_dict)
        print(f"Saved: {output_file}")
    elif ext == ".pickle":
        with open(output_file, "wb") as f:
            pickle.dump(out_df, f, protocol=pickle.HIGHEST_PROTOCOL)
            print(f"Saved: {output_file}")
    else:
        raise ValueError("Unsupported file format. Use .csv, .mat, or .pickle")
