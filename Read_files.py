
from pathlib import Path
import pandas as pd


startpath = Path(r'C:\Users\gdonno\Desktop\Hackathon\innovaid_hackathon_anima\input')

filelist = list(startpath.glob('**/*.csv') )      

pd.read_csv(filelist[0])

