#!/bin/bash
BASE="/Users/agoraqa/Desktop/lag/edit"
FILES="${BASE}/*.mov"

for f in $FILES
do
  dname=${f%.mov}.csv
  echo "Processing $f file..."
  python3 gaussian.py -i $f
done
