# Video-lag-tool
Draw a line on video, record the sum of pixel value from the line frame by frame throughout the whole video. If video freeze, the TOTAL_PIX_VALUE will remain unchanged for more than two frames.

## Packages
OpenCV, pandas, numpy

## Extract data from video
Usage:
```
python3 extract_data.py -i <input file>
```
Pixel line data that extracted from the video will be saved into **video_data.csv** file. Use -o flag to save to your own output directory.

## Data filtering
Usage:
```
python3 data_filter.py -i <input file> -n <optional threshold value>
```
to filter out lagging start time, end time and time period from **video_data.csv** file and save to **result.csv**. Use -o flag to save to your own output directory. Optional threshold value controls number of frames need to be filtered out, default value: 7.
