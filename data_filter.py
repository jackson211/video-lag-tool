import pandas as pd
import numpy as np

# Loading data and calculate the difference of TOTAL_PIX_VALUE between rows
df = pd.read_csv("video_data.csv")
df['PIX_VALUE_DIFF'] = df['TOTAL_PIX_VALUE'].diff()

# Return a list of index of continuously repeated 0
def zero_runs(a):
    # Create an array that is 1 where a is 0, and pad each end with an extra 0.
    iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(iszero))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges

THRESHOLD = 7 # lag for more than 7 frames
# Filtering lagging frame more than certain number
time_period = zero_runs(df['PIX_VALUE_DIFF'].tolist())
filtered_time_period = []
for i in range(len(time_period)):
    if time_period[i][1] - time_period[i][0] + 1 >= THRESHOLD:
        filtered_time_period.append(time_period[i])

# Output result dataframe
result = pd.DataFrame(columns=['START_TIME', 'END_TIME', 'TIME_PERIOD'])
for i in range(0, len(filtered_time_period)):
    start_time = df.iloc[filtered_time_period[i][0]-1]['TIME']
    end_time = df.iloc[filtered_time_period[i][1]]['TIME']
    time_diff = end_time - start_time
    result = result.append({'START_TIME': start_time, 'END_TIME': end_time, 'TIME_PERIOD': time_diff}, ignore_index=True)

result.to_csv('result.csv')
