#%%

from pathlib import Path
import pandas as pd


startpath = Path(r'C:\Users\gdonno\Desktop\Hackathon\innovaid_hackathon_anima\input')
output_path = Path(r'')

filelist = list(startpath.glob('**/*.csv') )      


for elem in filelist[0:1]:
    complete_ds = pd.read_csv(elem)
    complete_ds.describe()

    # order by timestamp
    complete_ds = complete_ds.sort_values(by='TIMESTAMP')

    # calculate timediff 
    diff_series = complete_ds['TIMESTAMP'].diff().dropna() .astype(int) # Drop NaN for the first element
    time_sampl = diff_series.value_counts().idxmax()

    # create new timestamp
    complete_ds['TIME'] = complete_ds.index*time_sampl

    # create subset, save
    subset = complete_ds.loc[ :, [ 'TIME', 'IMAGE_POSITION', 'IMAGE_TYPE', 'SCENE_INDEX']] 

    output_path = Path(str(elem).replace('input', 'subset') )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    subset.to_csv(output_path)


# %%
