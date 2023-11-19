from pathlib import Path

import pandas as pd
from tqdm import tqdm


def load_single(path: Path) -> pd.DataFrame:
    """
    Load data from a csv file
    :param path: path to the csv file
    :return: a pandas dataframe
    """
    df = pd.read_csv(path)

    return df


def load_set(path: Path) -> pd.DataFrame:
    """
    Load data from a csv file
    :param path: path to the csv file
    :return: a pandas dataframe
    """
    samples = []

    files = [x.resolve() for x in path.iterdir() if x.is_file()]
    print(f"Found {len(files)} files")

    for file in (prog_bar:= tqdm(files, total=len(files), desc="Loading samples")):
        prog_bar.set_description(f"Loading {file.stem}")
        sample = load_single(file)
        sample["SESSIONID"] = file.stem
        times = sample["TIME"].unique()
        time_map = {time: idx for idx, time in enumerate(times)}
        sample["TIME"] = sample["TIME"].map(time_map)
        samples.append(sample)

    samples = pd.concat(samples, ignore_index=True)
    samples.set_index(["SESSIONID", "TIME"], inplace=True)
    return samples
