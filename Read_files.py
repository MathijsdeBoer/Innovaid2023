#%%

from pathlib import Path
import pandas as pd
import numpy as np

startpath = Path(r'C:\Users\gdonno\Desktop\Hackathon\innovaid_hackathon_anima\input')
output_path = Path(r'')

filelist = list(startpath.glob('**/*.csv') )      

out_file_path = Path('/', startpath.parent,'output.csv') 
score_df = pd.read_csv(out_file_path)


#%%

# outliers

conditions_PHQ9 = [
    (score_df['PHQ9'] > 0 ) & (score_df['PHQ9'] < 4  ),
    (score_df['PHQ9'] > 4 ) & (score_df['PHQ9'] < 9  ),
    (score_df['PHQ9'] > 9 ) & (score_df['PHQ9'] < 14 ),
    (score_df['PHQ9'] > 14 )
]
conditions_BDI = [
    (score_df['BDI'] > 0  ) & (score_df['BDI'] < 9   ),
    (score_df['BDI'] > 9  ) & (score_df['BDI'] < 18  ),
    (score_df['BDI'] > 18 ) & (score_df['BDI'] < 29  ),
    (score_df['BDI'] > 29 ) 
]

values = ['min', 'mild', 'moderate', 'mod_severe']


score_df['PHQ9_%'] = score_df['PHQ9']* 100/ 63
score_df['BDI_%' ] = score_df['BDI' ]* 100/ 27
score_df['PHQ9_%'] = score_df['PHQ9_%'].astype(int)
score_df['BDI_%' ] = score_df['BDI_%' ].astype(int)


# Create a new column 'RANGE_PHQ9' based on conditions
score_df['RANGE_PHQ9'] = np.select(conditions_PHQ9, values, default='unknown')
score_df['RANGE_BDI']  = np.select(conditions_BDI,  values, default='unknown')


# Display the DataFrame
print(score_df)

#%%

# subset of input

for elem in filelist[0:5]:

    series_id = elem.stem

    index_containing_ddd = score_df[score_df['sid'].str.contains(series_id)].index[0]
    
    complete_ds = pd.read_csv(elem)


    # order by timestamp
    complete_ds = complete_ds.sort_values(by='TIMESTAMP')

    # calculate timediff 
    diff_series = complete_ds['TIMESTAMP'].diff().dropna() .astype(int) # Drop NaN for the first element
    time_sampl = diff_series.value_counts().idxmax()

    # create new timestamp
    complete_ds['TIME'] = complete_ds.index*time_sampl

    # create subset, save
    subset = complete_ds.loc[ :, [ 'TIME', 'IMAGE_POSITION', 'IMAGE_TYPE', 'SCENE_INDEX']]
    subset['RANGE_BDI'] = score_df.loc[ index_containing_ddd, 'RANGE_BDI'] 
    subset= subset.fillna("NONE")
    pd.unique(subset['IMAGE_TYPE'])

    output_path = Path(str(elem).replace('input', 'subset') )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subset.to_csv(output_path, index = False)

#%%



# %%

