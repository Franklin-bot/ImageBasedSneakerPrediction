# Image-Based Sneaker Resell Price Prediction

The sneaker resell market was worth an estimated $10.6 billion in 2022. The aim of this project is to identify potentially profitable sneakers by developing a machine learning model to accurately predict the future resell prices. While previous studies have attempted this by predicting price based on tabular data such as brand and shoe size, my model achieves higher accuracy predicting based on the sneakers' images.

## Rationale
Theoretically, models trained with images will perform better than those trained with just tabular data, since for sneakers, like art, value is highly correlated with design. This model extracts features from sneaker images and conducts regression with this information.

## Data
The dataset was collected by webscraping StockX.com; it consists of images and current resell prices for all ~293,000 different sneakers sold on StockX. 
Images: 128 x 128, jpg.

## Model
![Model (3)](https://github.com/Franklin-bot/ImageBasedSneakerPrediction/assets/63462715/e8bbce3f-6a67-489b-8397-cdda19b771f5)

## Results
Trained with Google Colab.\
<img width="603" alt="Screenshot 2023-08-19 at 3 56 45 PM" src="https://github.com/Franklin-bot/ImageBasedSneakerPrediction/assets/63462715/9f85fc78-4760-4151-a92d-8c40a476435f">

## Deployment
Sneaker prices are constantly changing, and the model must continuously retrain to maintain its accuracy. To do this, I created an auto ML pipeline that can automatically collect new data, process it, and retrain the model when run. \
\
The pipeline is dockerized and deployed with kubernetes via Kubeflow on AWS, utilizing EKS clusters, EC2 instances, and S3 storage. This allows for real-time optimization/scaling (up to 10 m5.large instances), drift monitoring, and automated continuous learning.


