#!/bin/bash
BASE="/Users/agoraqa/Desktop/2.2主版本/lag_videos/iphone7/edit"
FILES="${BASE}/*.mov"

for f in $FILES
do
  dname=${f%.mov}.csv
  # result_name=${f%.mov}_result.csv
  echo "Processing $f file..."
  python3 gaussian.py -i $f -o $dname
  # echo "Cleaning $dname file..."
  # python3 data_filter.py -i $dname -o $result_name
  # take action on each file. $f store current file name
  # echo "Saved to $result_name."
done
