from kfp import components, compiler
from kfp.v2 import dsl
from kfp.v2.dsl import component
from kfp.v2.dsl import (
    Input,
    Output,
    Artifact,
    Dataset,
)

from components.data_collection import collect_data
from components.data_processing import process_data

@component(base_image='153555882801.dkr.ecr.us-east-2.amazonaws.com/sneaker-cluster')
def data_collection_component():
    collect_data()

@component(base_image='153555882801.dkr.ecr.us-east-2.amazonaws.com/sneaker-cluster')
def data_processing_component():
    process_data()

@dsl.pipeline(name='sneaker-pipeline')
def my_pipeline():
    data_collection_component()
    data_processing_component()

if __name__ == '__main__':
    compiler.Compiler().compile(my_pipeline, package_path='/Users/FranklinZhao/TensorFlowProjects/ImageBasedSneakerPrediction/deployment/pipeline.yaml')

