import numpy as np
import pandas as pd
import cv2
import argparse

N = 100 # Number of sampling points
X_MIN = 500 # Coordinates for sampling area
X_MAX = 800
Y_MIN = 350
Y_MAX = 600
SEED = 1234 # Initialize random state

def gaussian_filter():
    np.random.seed(SEED)
    x = np.random.randint(X_MIN, X_MAX, size=(N, 1))
    y = np.random.randint(Y_MIN, Y_MAX, size=(N, 1))
    return np.concatenate((x, y), axis=1)

def get_pix_value(frame, f):
    pix_value = []
    for n in f:
        pix_value.append(frame[n[1], n[0]])
    return np.asarray(pix_value, dtype=np.int16)

def get_data(INPUT, OUTPUT, filter):
    df = pd.DataFrame(columns=['PIX_VALUE_DIFF'])
    df.index.name = 'FRAME'

    cap = cv2.VideoCapture(INPUT[0].name)
    previous_value = None
    # np.empty([N, 1], dtype=np.int16)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
            print("Frame: ", frame_num)

            # Calculate the difference between current and previous frames
            current_value = get_pix_value(gray, filter)
            if previous_value is None:
                df.loc[frame_num] = 0
            else:
                diff = sum(np.abs(current_value-previous_value))
                df.loc[frame_num] = diff
                print(diff)
            previous_value = current_value

            # Draw corresponding gaussian points
            for coor in filter:
                cv2.circle(gray, tuple(coor), 1, (255, 255, 255))
            cv2.imshow('frame',gray)

            # Frame display time and quit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else: break
    cap.release()
    cv2.destroyAllWindows()
    return df.to_csv(OUTPUT)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs=1, type=argparse.FileType('r'), help="Directory of input file")
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w'), help="Directory of output file")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output if args.output is not None else 'video_data.csv'

    filter = gaussian_filter()
    get_data(input_file, output_file, filter)

    print('Video data has been collected!')
