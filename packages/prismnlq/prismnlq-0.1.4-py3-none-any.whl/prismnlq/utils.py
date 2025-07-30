import io
import json
import sys
import tarfile

import polars as pl
import pyarrow.parquet as pq
import requests
from tqdm import tqdm


def download(links):
    r = requests.get(url=links, stream=True)
    #print("Downloading")
    r.raise_for_status()
    result = []
    with tqdm(desc="Downloading", total=int(r.headers["content-length"]), unit="B", unit_scale=True, unit_divisor=1024) as pbar:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk is not None:  # filter out keep-alive new chunks
                result.append(chunk)
                pbar.update(len(chunk))
                sys.stdout.flush()  # Ensure the output is flushed
    result = b"".join(result)

    return result


def unzip_tar(content, data_type):
    dfs = {}
    tar_obj = tarfile.open(fileobj=io.BytesIO(content), mode='r')
    fname = tar_obj.getnames()
    metadata = None
    if fname is None: fname = []
    for name in fname:
        f = tar_obj.extractfile(name).read()
        if ".txt" in name:
            metadata = json.loads(f)
        else:
            if data_type=='pandas':
                obj = pq.read_table(io.BytesIO(f))
                dfs[name] = obj.to_pandas()
            elif data_type=='polars':
                dfs[name] = pl.read_parquet(io.BytesIO(f))
            else:
                raise ValueError(f'Invalid data_type: {data_type}')

    return dfs, metadata