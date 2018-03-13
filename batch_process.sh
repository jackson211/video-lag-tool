#!/bin/bash
BASE="/Users/agoraqa/Desktop/videos/iOS/test2"
V_FILES="${BASE}/*.mov"
D_FILES="${BASE}/*.csv"
for f in $V_FILES
do
  dname=${f%.mov}.csv
  result_name=${f%.mov}_result.csv
  echo "Processing $f file..."
  python3 extract_data.py -i $f -o $dname
  echo "Cleaning $dname file..."
  python3 data_filter.py -i $dname -o $result_name
  # take action on each file. $f store current file name
  echo "Saved to $result_name."
done