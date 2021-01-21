# Tools

## plot.py

To plot PM2.5 values over the last 10 days for the 216b9a source:

```
$ python3 tools/plot.py --endpoint https://rald-dev.greenbeep.com/api/v1/measurements --source 216b9a --days 10 --output output.png
```

To also visualize it:

```
$ python3 tools/plot.py --endpoint https://rald-dev.greenbeep.com/api/v1/measurements --source 216b9a --days 10 --output output.png --visualize
```
