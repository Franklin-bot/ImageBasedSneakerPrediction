def process_data():

    import pandas as pd
    import numpy as np
    import json
    from tqdm.auto import tqdm
    from tqdm import tqdm

    import boto3
    s3 = boto3.resource('s3')
    df_ori = pd.read_csv('s3://sneaker-dataset/5000_output.csv')
    df = df_ori.copy()

    # remove unnecessary data
    cols_to_drop = ['urlKey', 'id', 'name', 'description', 'model', 'market', 'condition', 'productCategory', 'listingType', 'browseVerticals', 'favorite', 'variants']
    df = df.drop(cols_to_drop, axis=1)

    # remove rows with missing data
    df = df.dropna(axis=0, how='any')
 
    import asyncio
    import aiohttp
    import cv2
    import numpy as np
    from tqdm.asyncio import tqdm_asyncio
    import nest_asyncio
    nest_asyncio.apply()

    async def openImage(url, session):
        async with session.get(url) as response:
            image = await response.read()
            image_np = np.asarray(bytearray(image), dtype="uint8")
            image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
            image_np = None
            image = cv2.resize(image, (128, 128), interpolation=cv2.INTER_AREA)
            return image

    async def process_images(urls):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.create_task(openImage(url, session))
                tasks.append(task)
            results = await tqdm_asyncio.gather(*tasks)
        return results

    async def main(df):
        img_urls = df['imageUrl'].tolist()
        result_images = await process_images(img_urls)
        return result_images

    img_df = asyncio.run(main(df))


    import io
    import pickle

    # upload pickled image data to s3
    s3_client = boto3.client('s3')
    img_df_data = io.BytesIO()
    pickle.dump(img_df, img_df_data)
    img_df_data.seek(0)
    s3_client.upload_fileobj(img_df_data, 'sneaker-dataset', '5000_images.pkl')

    prices_df = np.asarray(df['last sale'])
    prices_df_data = io.BytesIO()
    pickle.dump(prices_df, prices_df_data)
    prices_df_data.seek(0)
    s3_client.upload_fileobj(prices_df_data, 'sneaker-dataset', '5000_prices.pkl')

    
