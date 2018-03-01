# Video-lag-tool
Draw a line on video, record the sum of pixel value from the line frame by frame throughout the whole video. If video freeze, the TOTAL_PIX_VALUE will remain unchanged for more than two frames.

## Packages
OpenCV, pandas, numpy

## Extract data from video
Modify **VIDEO_DIR** to use your own video. Then run:
```
python3 extract_data.py
```
Pixel line data that extracted from the video will be saved into **video_data.csv** file.

## Data filtering
Run:
```
python3 data_filter.py
```
to filter out lagging start time, end time and time period from **video_data.csv** file and save to **result.csv**.
