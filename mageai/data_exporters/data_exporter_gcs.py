from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from pandas import DataFrame
from os import path

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    """
    this block is used to export the DF from the previous block to S3. This is to demonstrate data ingestion to S3 lake and save the final file as Amazon.csv
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'

    bucket_name = 'magezc-ken-demo'
    object_key = 'capstone/raw/customer-support-tickets.csv'

    GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
        df,
        bucket_name,
        object_key,
    )
