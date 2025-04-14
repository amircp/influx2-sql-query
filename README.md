# InfluxDB InfluxQL Python Client

A lightweight Python client for querying InfluxDB using InfluxQL (SQL-like query language) and transforming results into pandas DataFrames.

## Overview

This package provides a simple client to connect to InfluxDB, execute InfluxQL queries, and easily transform the results into Python data structures including pandas DataFrames. It's designed to be simple and efficient for data analysis workflows.

## Features

- Connect to InfluxDB instances using token authentication
- Execute InfluxQL queries
- Convert query results to pandas DataFrames
- Support for JSON data format
- Efficient HTTP communication via httpx

## Requirements

- Python 3.6+
- httpx
- pandas

## Installation

```bash
pip install -r requirements.txt
```


## Enabling the InfluxQL API in InfluxDB

Before using this client, you need to ensure that the InfluxQL API is enabled in your InfluxDB instance:
Please follow this guide https://docs.influxdata.com/influxdb/v2/query-data/influxql/


or try running this setting in Docker image:

1. **Configuration File Method**:
   Edit your influxdb configuration file (usually `influxdb.conf`) and ensure the following settings:
   
   ```
   [influxql]
     enabled = true
   ```


2. **Environment Variable Method**:
   Set the following environment variable when starting InfluxDB:
   
   ```
   INFLUXDB_INFLUXQL_ENABLED=true
   ```

3. **Docker Setup**:
   If you're using Docker, add the environment variable to your docker-compose.yml or docker run command:
   
   ```yaml
   # docker-compose.yml example
   services:
     influxdb:
       image: influxdb:latest
       environment:
         - INFLUXDB_INFLUXQL_ENABLED=true
   ```

## Usage

### Basic Setup

```python
from influxdb2client import InfluxQLClient

# Configure connection details
token = "your-influxdb-token"
url = "http://localhost:8086"  # Your InfluxDB URL
bucket = "your-bucket-name"    # InfluxDB bucket name

# Create client instance
influx_client = InfluxQLClient(host=url, bucket=bucket, token=token)
```

### Executing Queries and Getting Results as DataFrame

```python
# Execute a query and convert results to a DataFrame
query = """
SELECT last(change_percent_24) as Change, 
       last(price_close) as Price, 
       last(ticker) as ticker 
FROM market24 
WHERE symbol =~ /USDT/ 
  AND time > now()-24h 
  AND change_percent_24 > 3 
GROUP BY symbol 
ORDER BY time
"""

df = influx_client.query(query).as_dataframe()

# Now you can work with the pandas DataFrame
print(df.head())

# Example: Extract unique ticker values
symbols = set(df['ticker'].values)
for symbol in symbols:
    if symbol is not None:
        print(symbol)
```

### Getting Query Results as JSON

```python
# Get query results as JSON
json_data = influx_client.query(query).as_json()
print(json_data)
```

## Error Handling

The client will raise appropriate HTTP exceptions if the query fails:

```python
try:
    result = influx_client.query("SELECT * FROM nonexistent_measurement").as_dataframe()
except Exception as e:
    print(f"Query failed: {e}")
```

## Example Script

```python
from influxdb2client import InfluxQLClient

# Configuration
token = "1ssd0mS1dGZRddr52BdwST1gt5IVt-umO4MjEaENSS5kvaYogC7WaVh8L2oiAWRzT2LMAp4v1QTASMoRQUmks6yg=="
url = "http://localhost:8086"
bucket = "binance"

# Initialize client
influx_client = InfluxQLClient(host=url, bucket=bucket, token=token)

# Query data for cryptocurrencies with >3% change in the last 24h
df = influx_client.query("""
    SELECT last(change_percent_24) as Change,
           last(price_close) as Price,
           last(ticker) as ticker 
    FROM market24 
    WHERE symbol =~ /USDT/ 
      AND time > now()-24h 
      AND change_percent_24 > 3
    GROUP BY symbol 
    ORDER BY time
""").as_dataframe()

# Print unique cryptocurrency symbols
symbols = set(df['ticker'].values)
for symbol in symbols:
    if symbol is not None:
        print(symbol)
```

## Limitations

- The current implementation is designed for simple query operations
- Complex queries with multiple result sets might require additional handling
- The client assumes successful API responses have a specific structure

## License

[MIT License](LICENSE)
