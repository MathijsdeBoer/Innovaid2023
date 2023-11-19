from pathlib import Path
import pandas as pd
import numpy as np
from tqdm import tqdm

startpath = Path(r'../Data/input/').resolve()
output_path = Path(r'../Data/preprocessed/samples').resolve()

filelist = [x.resolve() for x in startpath.iterdir() if x.is_file()]

gt_file = startpath.parent / 'output.csv' 
score_df = pd.read_csv(gt_file)

# outliers

conditions_PHQ9 = [
    (score_df['PHQ9'] >= 0  ) & (score_df['PHQ9'] < 4  ),
    (score_df['PHQ9'] >= 4  ) & (score_df['PHQ9'] < 9  ),
    (score_df['PHQ9'] >= 9  ) & (score_df['PHQ9'] < 14 ),
    (score_df['PHQ9'] >= 14 )
]
conditions_BDI = [
    (score_df['BDI'] >= 0  ) & (score_df['BDI'] < 9   ),
    (score_df['BDI'] >= 9  ) & (score_df['BDI'] < 18  ),
    (score_df['BDI'] >= 18 ) & (score_df['BDI'] < 29  ),
    (score_df['BDI'] >= 29 ) 
]

values = ['min', 'mild', 'moderate', 'mod_severe']


score_df['PHQ9_%'] = score_df['PHQ9']* 100/ 27
score_df['BDI_%' ] = score_df['BDI' ]* 100/ 63
score_df['PHQ9_%'] = score_df['PHQ9_%'].astype(int)
score_df['BDI_%' ] = score_df['BDI_%' ].astype(int)


# Create a new column 'RANGE_PHQ9' based on conditions
score_df['RANGE_PHQ9'] = np.select(conditions_PHQ9, values, default='unknown')
score_df['RANGE_BDI']  = np.select(conditions_BDI,  values, default='unknown')


# Display the DataFrame
print(score_df)

# Remove outliers
 
diffs = abs( score_df['PHQ9_%'] - score_df['BDI_%' ]) 

Q1 = diffs.quantile(0.25)
Q3 = diffs.quantile(0.75)
IQR = Q3 - Q1

lower_threshold = Q1 - 1.5 * IQR
upper_threshold = Q3 + 1.5 * IQR

# Mask for rows within the IQR range
within_iqr_mask = (diffs >= lower_threshold) & (diffs <= upper_threshold)

# Keep only rows within the IQR range
filtered_score_df = score_df[within_iqr_mask]
# filtered_score_df = score_df[~(within_iqr_mask)]

# subset of input

for elem in tqdm(filelist):

    series_id = elem.stem

    idx_remove = score_df[score_df['sid'].str.contains(series_id)].index[0]
    
    complete_ds = pd.read_csv(elem)


    # order by timestamp
    complete_ds = complete_ds.sort_values(by='TIMESTAMP')

    # calculate timediff 
    diff_series = complete_ds['TIMESTAMP'].diff().dropna() .astype(int) # Drop NaN for the first element
    time_sampl = diff_series.value_counts().idxmax()

    # create new timestamp
    complete_ds['TIME'] = complete_ds.index*time_sampl

    # create subset, save
    subset = complete_ds.loc[ :, [ 'TIME', 'IMAGE_POSITION', 'IMAGE_TYPE', 'SCENE_INDEX', 'RX', 'RY']]
    subset['RANGE_BDI'] = score_df.loc[ idx_remove, 'RANGE_BDI'] 
    subset= subset.fillna("NONE")
    pd.unique(subset['IMAGE_TYPE'])

    out_file = output_path / elem.name
    output_path.mkdir(parents=True, exist_ok=True)
    subset.to_csv(out_file, index = False)
