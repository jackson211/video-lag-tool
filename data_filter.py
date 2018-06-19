import pandas as pd
import numpy as np
import argparse
import os
from graph import run

PIX_ERROR = 10000

# Return a list of index of continuously repeated 0
def zero_runs(a):
    # Create an array that is 1 where a is 0, and pad each end with an extra 0.
    iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(iszero))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges

def clean_data(INPUT, THRESHOLD):
    # Loading data and calculate the difference of TOTAL_PIX_VALUE between rows
    for file in INPUT:
        df = pd.read_csv(file)
        dir = os.path.dirname(file.name)
        filename, extension = os.path.basename(file.name).split('.')

        clean_dir = dir + '/clean'
        result_dir = dir + '/result'
        clean_file = filename + '-clean.' + extension
        result_file = filename + '-result.' + extension

        if not os.path.exists(clean_dir):
            os.makedirs(clean_dir)
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        df.loc[(df['PIX_VALUE_DIFF'] <= PIX_ERROR), 'PIX_VALUE_DIFF'] = 0 # Filtering out difference value <=1000
        df.to_csv(os.path.join(clean_dir, clean_file))

        # Filtering lagging frame more than certain number
        time_period = zero_runs(df['PIX_VALUE_DIFF'].tolist())-1
        time_period[0, :1] = 0
        filtered_time_period = time_period[np.where(np.diff(time_period)+1 > THRESHOLD)[0]]

        #Output result dataframe
        result = pd.DataFrame(columns=['START_FRAME', 'END_FRAME', 'FRAME_PERIOD'])

        for i in range(0, len(filtered_time_period)):
            start_frame = df.iloc[filtered_time_period[i][0]]['FRAME']
            end_frame = df.iloc[filtered_time_period[i][1]]['FRAME']
            frame_diff = end_frame - start_frame + 1
            result = result.append({'START_FRAME': start_frame, 'END_FRAME': end_frame, 'FRAME_PERIOD': frame_diff}, ignore_index=True)

        print(result)
        result.to_csv(os.path.join(result_dir, result_file))
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
    |   | '` ,/    ;   :    /  |   | '`--'  |   |    |
    ;   :  .'       \   \ .'   '   : |      |   :   .'
    |   ,.'          `---`     ;   |.'      |   | ,'
    '---'                      '---'        `----'
    """
    return done


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', nargs='*', type=argparse.FileType('r'), help="Directory of input file.")
    parser.add_argument('-n', '--threshold', nargs='?', type=int, help="Threshold value that set number of frames need to be filtered out. Default value: 7.")
    args = parser.parse_args()

    input_files = args.input
    threshold = args.threshold if args.threshold is not None else 6

    print(clean_data(input_files, threshold))
    run(input_files)
