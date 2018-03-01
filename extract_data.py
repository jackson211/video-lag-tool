import numpy as np
import pandas as pd
import cv2

VIDEO_DIR = '/Users/YOUR/OWN/VIDEO/DIR'
cap = cv2.VideoCapture(VIDEO_DIR)

# Config for the line coordinates and size of the line
X = 375
Y = 589
SIZE =  100

df = pd.DataFrame(columns=['TOTAL_PIX_VALUE'])
df.index.name = 'TIME'

while(cap.isOpened()):
    ret, frame = cap.read()

    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC)/1000

    total = 0
    if frame is None:
        break
    else:
        for value in range(0, SIZE+1):
            total += sum(frame[Y + value, X]) #row major order in opencv

    df.loc[current_time] = [total]
    print("Time: {0}, Pixel Value: {1}".format(current_time, total))

    # Draw corresponding line from ((X, Y), (X, Y + SIZE))
    cv2.line(frame, (X, Y), (X, Y + SIZE),(255,255,255),1)
    cv2.imshow('frame',frame)
    print(df.tail())

    # Frame rate
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0}".format(fps))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
df.to_csv('video_data.csv')
