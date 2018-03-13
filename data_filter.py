import pandas as pd
import numpy as np
import argparse
from tqdm import tqdm

THRESHOLD = 11 # lag for more than 11 frames

# Return a list of index of continuously repeated 0
def zero_runs(a):
    # Create an array that is 1 where a is 0, and pad each end with an extra 0.
    iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(iszero))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges

def clean_data(INPUT, OUTPUT):
    # Loading data and calculate the difference of TOTAL_PIX_VALUE between rows
    df = pd.read_csv(INPUT[0])
    df['PIX_VALUE_DIFF'] = df['TOTAL_PIX_VALUE'].diff()
    df.loc[(df['PIX_VALUE_DIFF'] <= 100) & (df['PIX_VALUE_DIFF'] >= -100), 'PIX_VALUE_DIFF'] = 0 # Filtering out difference value <=100 and >=-100
    df = df.fillna(0)

    # Filtering lagging frame more than certain number
    time_period = zero_runs(df['PIX_VALUE_DIFF'].tolist())-1
    time_period[0, :1] = 0
    filtered_time_period = time_period[np.where(np.diff(time_period)+1 >= THRESHOLD)[0]]

    #Output result dataframe
    result = pd.DataFrame(columns=['START_TIME', 'END_TIME', 'TIME_PERIOD'])
    for i in range(0, len(filtered_time_period)):
        start_time = df.iloc[filtered_time_period[i][0]]['TIME']
        end_time = df.iloc[filtered_time_period[i][1]]['TIME']
        time_diff = end_time - start_time
        result = result.append({'START_TIME': start_time, 'END_TIME': end_time, 'TIME_PERIOD': time_diff}, ignore_index=True)

    return result.to_csv(OUTPUT)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs=1, type=argparse.FileType('r'), help="Directory of input file.")
    parser.add_argument('-o', '--output', nargs='?', type=argparse.FileType('w'), help="Directory of output file.")
    parser.add_argument('-n', '--threshold', nargs='?', type=int, help="Threshold value that set number of frames need to be filtered out. Default value: 7.")
    args = parser.parse_args()

    input_file = args.input
    output_file = args.output if args.output is not None else 'result.csv'
    THRESHOLD = args.threshold if args.threshold is not None else 11
    clean_data(input_file, output_file)
    done = """\
                     ,----..            ,--.
        ,---,       /   /   \         ,--.'|    ,---,.
      .'  .' `\    /   .     :    ,--,:  : |  ,'  .' |
    ,---.'     \  .   /   ;.  \,`--.'`|  ' :,---.'   |
    |   |  .`\  |.   ;   /  ` ;|   :  :  | ||   |   .'
    :   : |  '  |;   |  ; \ ; |:   |   \ | ::   :  |-,
    |   ' '  ;  :|   :  | ; | '|   : '  '; |:   |  ;/|
    '   | ;  .  |.   |  ' ' ' :'   ' ;.    ;|   :   .'
    |   | :  |  ''   ;  \; /  ||   | | \   ||   |  |-,
    '   : | /  ;  \   \  ',  / '   : |  ; .''   :  ;/|
    |   | '` ,/    ;   :    /  |   | '`--'  |   |    \\
    ;   :  .'       \   \ .'   '   : |      |   :   .'
    |   ,.'          `---`     ;   |.'      |   | ,'
    '---'                      '---'        `----'
    """
    print(done)
