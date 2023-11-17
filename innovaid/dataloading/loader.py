from pathlib import Path

import pandas as pd


def load_single(path: Path) -> pd.DataFrame:
    """
    Load data from a csv file
    :param path: path to the csv file
    :return: a pandas dataframe
    """
    return pd.read_csv(path)


def load_set(path: Path) -> pd.DataFrame:
    """
    Load data from a csv file
    :param path: path to the csv file
    :return: a pandas dataframe
    """
    samples = None

    files = [x for x in path.iterdir() if x.is_file()]

    for file in files:
        if samples is None:
            samples = load_single(file)
            samples["SessionID"] = file.stem
        else:
            sample = load_single(file)
            sample["SessionID"] = file.stem
            samples = samples.concat(sample)

    return samples


def load_gt(path: Path) -> pd.DataFrame:
    """
    Load data from a csv file
    :param path: path to the csv file
    :return: a pandas dataframe
    """
    return pd.read_csv(path)