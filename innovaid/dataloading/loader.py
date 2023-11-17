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

    for idx, file in (prog_bar:= tqdm(enumerate(files), total=len(files), desc="Loading samples")):
        prog_bar.set_description(f"Loading {file.stem}")
        sample = load_single(file)
        sample["SESSIONID"] = idx
        times = sample["TIME"].unique()
        sample["TIME"] = sample["TIME"].apply(lambda x: times.tolist().index(x))
        samples.append(sample)

    samples = pd.concat(samples, ignore_index=True)
    samples.set_index(["SESSIONID", "TIME"], inplace=True)
    return samples


def load_gt(path: Path) -> pd.DataFrame:
    """
    Load data from a csv file
    :param path: path to the csv file
    :return: a pandas dataframe
    """
    return pd.read_csv(path)