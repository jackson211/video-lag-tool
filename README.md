# Video-lag-tool
Video freeze analysis

## Packages
OpenCV, pandas, numpy

## Extract data from video
Usage:
```
python3 gaussian.py -i <input file>
```
Pixel data that extracted from the video will be saved into **.csv** file. Use -o flag to save to your own output directory.

## Data filtering
Usage:
```
python3 data_filter.py -i <input file> -n <optional threshold value>
```
to filter out lagging start time, end time and time period from raw csv file and save to **result.csv**. Use -o flag to save to your own output directory. Optional threshold value controls number of frames need to be filtered out, default value: 7.
