from google.cloud import storage
import glob
import pandas as pd
import os


def download_blob(proj = "redditPredict", bucket_name = "2014_funny_bucket", folder = "data/temp/"):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client(project=proj)

    bucket = storage_client.bucket(bucket_name)

    blobs = bucket.list_blobs(prefix = "2014_funny_comment_")
    for blob in blobs:
        print(blob.name)
        destination_uri = f"{folder}/{blob.name}"
        blob.download_to_filename(destination_uri)
    
    
download_blob()
  
filenames = [i for i in glob.glob(f"*.csv")]
dfs = []
for filename in filenames:
    print(filename)
    dfs.append(pd.read_csv(filename, index_col = None, header = 0))
bigdf = pd.concat(dfs, axis = 0, ignore_index = True)


bigdf.to_csv("2014_funny_comments.csv", index = False)
