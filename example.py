token = "1ssd0mS1dGZRddr52BdwST1gt5IVt-umO4MjEaENSS5kvaYogC7WaVh8L2oiAWRzT2LMAp4v1QTASMoRQUmks6yg=="
url = "http://localhost:8086"
bucket = "binance"

influx_client = InfluxQLClient(host=url, bucket=bucket, token=token)


df = influx_client.query("SELECT last(change_percent_24)  as Change,  last(price_close) as Price, last(ticker) as ticker FROM market24 WHERE symbol =~ /USDT/  and time > now()-24h and change_percent_24 > 3   group by symbol order by time  ").as_dataframe()

symbols = (set(df['ticker'].values))

for i in symbols:
    if i is not None:
        print(i)