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
    df["SESSIONID"] = path.stem

    # Set path name and TimeStamp as index
    df.set_index(["SESSIONID", "TIME"], inplace=True)

    return df


def load_set(path: Path) -> pd.DataFrame:
    """
    Load data from a csv file
    :param path: path to the csv file
    :return: a pandas dataframe
    """
    samples = None

    files = [x.resolve() for x in path.iterdir() if x.is_file()]
    print(f"Found {len(files)} files")

    for file in tqdm(files, desc="Loading samples"):
        if samples is None:
            samples = load_single(file)
        else:
            pd.concat([samples, load_single(file)])

    return samples


def load_gt(path: Path) -> pd.DataFrame:
    """
    Load data from a csv file
    :param path: path to the csv file
    :return: a pandas dataframe
    """
    return pd.read_csv(path)