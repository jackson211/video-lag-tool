import numpy as np
import pandas as pd
import cv2
import argparse

# Config for the line coordinates and size of the line
X = 650
Y = 425
SIZE =  100

X_2 = 750
Y_2 = 300
SIZE_2 = 100

def get_data(INPUT, OUTPUT):
    df = pd.DataFrame(columns=['TOTAL_PIX_VALUE'])
    df.index.name = 'TIME'

    cap = cv2.VideoCapture(INPUT[0].name)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
            # fps = cap.get(cv2.CAP_PROP_FPS)
            # convert_frame = str(int(current_frame/fps)) + ":" + str(int(current_frame%30))

            total = 0
            for value in range(0, SIZE+1): # 1st line
                total += gray[Y+value, X] #row major order in opencv
            for value_2 in range(0, SIZE_2+1): # 2nd line
                total += gray[Y_2+value_2, X_2]
            df.loc[frame_num] = [total]

            # Draw corresponding line from ((X, Y), (X, Y + SIZE))
            cv2.line(gray, (X, Y), (X, Y+SIZE),(255,255,255),1)
            cv2.line(gray, (X_2, Y_2), (X_2, Y_2+SIZE_2),(255,255,255),1)
            cv2.imshow('frame',gray)
            print(df.tail())

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

    get_data(input_file, output_file)
    print('Video data has been collected!')
