# Video-lag-tool
Video transition analysis

## Packages
OpenCV, pandas, numpy, bokeh

## Extract data from video
Usage:
```
python3 gaussian.py -i <input file>
```
Define your own sampling area(X_MIN, X_MAX, Y_MIN, Y_MAX) in **gaussian.py** Pixel data that extracted from the video will be saved into **.csv** files with same name as the input video files.

## Data filtering
Usage:
```
python3 data_filter.py -i <input file> -n <optional threshold value>
```
To filter out lagging start time, end time and time period from raw csv file and save to **result.csv**, cleaned data files, and visualization graph html file . Optional threshold value controls number of frames need to be filtered out, default value: 6.
