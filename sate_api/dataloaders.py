import os
import glob
import pandas
import requests
from tqdm import tqdm

def download(url: str, fname: str, chunk_size=1024):
    resp = requests.get(url, stream=True)
    total = int(resp.headers.get('content-length', 0))
    with open(fname, 'wb') as file, tqdm(
        desc=fname,
        total=total,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=chunk_size):
            size = file.write(data)
            bar.update(size)


def read_csvs(path:str,df):
    data=[pandas.read_csv(csv_file,encoding= 'unicode_escape') for path, subdir, _ in os.walk(path) for csv_file in glob.glob(os.path.join(path, "*.csv"))]
    df == pandas.concat(data, axis=0, ignore_index=True)
    return df 