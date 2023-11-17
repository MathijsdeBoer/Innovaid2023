#%%

from pathlib import Path
import pandas as pd
from tqdm import tqdm


startpath = Path(r'../data/input').resolve()
output_path = Path(r'../data/preprocessed/samples').resolve()

# filelist = list(startpath.glob('**/*.csv') )
filelist = [x.resolve() for x in startpath.iterdir() if x.is_file() and x.suffix == '.csv']

for elem in (prog_Bar := tqdm(filelist)):
    prog_Bar.set_description(f"Processing {elem.name}")
    complete_ds = pd.read_csv(elem)
    # complete_ds.describe()

    # order by timestamp
    complete_ds = complete_ds.sort_values(by='TIMESTAMP')

    # calculate timediff 
    diff_series = complete_ds['TIMESTAMP'].diff().dropna() .astype(int) # Drop NaN for the first element
    time_sampl = diff_series.value_counts().idxmax()

    # create new timestamp
    complete_ds['TIME'] = complete_ds.index*time_sampl

    # create subset, save
    subset = complete_ds.loc[ :, [ 'TIME', 'IMAGE_POSITION', 'IMAGE_TYPE', 'SCENE_INDEX', 'RX', 'RY']]
    subset= subset.fillna("NONE")

    output_file = output_path / elem.name
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    subset.to_csv(output_file, index = False)

