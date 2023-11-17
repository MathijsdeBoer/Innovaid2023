from pathlib import Path
import pandas as pd


startpath = Path(r'C:\Users\gdonno\Desktop\Hackathon\innovaid_hackathon_anima\input')

filelist = list(startpath.glob('**/*.csv') )      


for elem in filelist[0:1]:
    complete_ds = pd.read_csv(elem)
    complete_ds.describe()




