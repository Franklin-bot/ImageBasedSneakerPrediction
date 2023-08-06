import pandas as pd
import numpy as np
import json
import requests
import cv2
from tqdm.auto import tqdm
from tqdm import tqdm

# open raw data
file_path = "/Users/FranklinZhao/TensorFlowProjects/ImageBasedSneakerPrediction/data/rawoutput.csv"
df_ori= pd.read_csv(filepath_or_buffer=file_path, sep='\t', index_col=0)
df = df_ori.copy()

# remove unnecessary data
cols_to_drop = ['urlKey', 'id', 'name', 'description', 'model', 'market', 'condition', 'productCategory', 'listingType', 'browseVerticals', 'favorite', 'variants']
df = df.drop(cols_to_drop, axis=1)

# remove rows with missing data
df = df.dropna(axis=0, how='any')

# clean to extract image url and retail price
def cleanImageUrl(url):
    return (url.split('.jpg')[0]) + '.jpg'

df['imageUrl'] = df['media'].apply(lambda x: (json.loads(x.replace("\'", "\"")))["thumbUrl"])
df['imageUrl'] = df['imageUrl'].apply(cleanImageUrl)

df['retailPrice'] = df['productTraits'].apply(lambda x: (json.loads(x.replace("\'", "\""))[0]["value"]))
df = df.drop(['media', 'productTraits'], axis=1)

import asyncio
from tqdm.asyncio import tqdm_asyncio
import nest_asyncio
nest_asyncio.apply()

async def openImage(url):
    response = requests.get(url, stream=True).raw
    image = np.asarray(bytearray(response.read()), dtype="uint8")
    return cv2.imdecode(image, cv2.IMREAD_COLOR)

async def process_images(urls):
    tasks = [openImage(url) for url in urls]
    return await tqdm_asyncio.gather(*tasks)


async def main(df):
    img_urls = df['imageUrl'].tolist()
    result_images = await process_images(img_urls)
    return result_images

if __name__ == "__main__":
    asyncio.run(main(df))


