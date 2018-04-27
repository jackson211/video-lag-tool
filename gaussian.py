import numpy as np
import pandas as pd
import cv2
import argparse
import os
import math

N = 1000 # Number of sampling points
X_MIN = 20 # Coordinates for sampling area
X_MAX = 750
Y_MIN = 100
Y_MAX = 700
SEED = 1020 # Initialize random state

def gaussian_filter():
    np.random.seed(SEED)
    x = np.random.randint(X_MIN, X_MAX, size=(N, 1))
    y = np.random.randint(Y_MIN, Y_MAX, size=(N, 1))
    return np.concatenate((x, y), axis=1)

def get_pix_value(frame, f):
    pix_value = []
    for n in f:
        pix_value.append(frame[n[1], n[0]])
    return np.asarray(pix_value, dtype=np.int64)

def read_file(input):
    if isinstance(input, int):
        cap = cv2.VideoCapture(input)
    else:
        cap = cv2.VideoCapture(input.name)
    return cap

def pix_diff(curr, pre):
    # return sum(np.square(curr-pre, dtype=np.int64))
    return sum((curr-pre)**2)

def get_data(INPUT, OUTPUT, filter):
    df = pd.DataFrame(columns=['PIX_VALUE_DIFF'])
    df.index.name = 'FRAME'

    # file_name = INPUT.name
    cap = read_file(INPUT)
    previous_value = None

    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            print("Frame: ", i)

            # Calculate the difference between current and previous frames
            current_value = get_pix_value(gray, filter)
            if previous_value is None:
                df.loc[i] = 0
            else:
                diff = pix_diff(current_value, previous_value)
                df.loc[i] = diff
                print(diff)
            previous_value = current_value
            i+=1

            # Draw corresponding gaussian points
            for coor in filter:
                cv2.circle(gray, tuple(coor), 1, (255, 255, 255))
            cv2.imshow(str(INPUT), gray)

            # Frame display time and quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else: break
    cap.release()
    cv2.destroyAllWindows()
    return df.to_csv(OUTPUT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='*', type=argparse.FileType('r'), help="Directory of input file")
    args = parser.parse_args()

    filter = gaussian_filter()
    input_files = args.input
    if input_files is None:
        output_file = 'camera.csv'
        get_data(0, output_file, filter)
    else:
        for file in input_files:
            output_file = os.path.splitext(file.name)[0]+'.csv'
            get_data(file, output_file, filter)
            print('Video data has been collected!')
