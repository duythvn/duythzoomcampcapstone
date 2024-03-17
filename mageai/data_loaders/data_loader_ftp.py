from paramiko.client import SSHClient
from paramiko import AutoAddPolicy
from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader, ConfigKey
from os import path
import yaml
import os

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data(*args, **kwargs):
    """
    this block is used to download csv files from a folder (e.g: /test_core_data/tmp/), save them to a  local folder, then read through these files to create a main df
    the main df will be used by the next Data Export block to ingest data into S3
    there are obviously other methods to just download files via FTP and reupload files to S3 but we will be using this Data Ingestion approach for demonstrative purposes
    """
    # Specify your data loading logic here
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'dev'
    
    sftp_client = SSHClient()
    ftp_client.set_missing_host_key_policy(AutoAddPolicy())
    
    try:
        #FTP Details were removed 
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)  
            FTP_HOST = config[config_profile]['SFTP_HOST']
            FTP_PORT = config[config_profile]['SFTP_PORT']
            FTP_USER = config[config_profile]['SFTP_USER']
            FTP_PASSWORD = config[config_profile]['SFTP_PASSWORD']
    
   

        sftp_client = SSHClient()
        sftp_client.set_missing_host_key_policy(AutoAddPolicy())
        sftp_client.connect(hostname=FTP_HOST, port=FTP_PORT, username=FTP_USER, password=FTP_PASSWORD)
        sftp_handle = sftp_client.open_sftp()
#       Initialize an empty DataFrame
 
       
        remote_folder = '/test_core_data/tmp/'
        local_path ='./tmpfiles/'
        sftp_handle.chdir(remote_folder)
        files = sftp_handle.listdir()
        for file_name in files:
            print(file_name)
            if file_name.endswith('.csv'):
            remote_path = os.path.join(remote_folder, file_name)
            local_file_path = os.path.join(local_path, file_name)
            sftp_handle.get(remote_path, local_file_path)

        main_df = pd.DataFrame()

        # Iterate through files in the folder
        for file_name in os.listdir(local_path):
            if file_name.endswith(".csv"):
                print('ok')
                file_path = os.path.join(local_path,file_name)

                # Read the CSV file into a DataFrame
                df = pd.read_csv(file_path)

                # # Append the DataFrame to the main DataFrame
                main_df = pd.concat([main_df, df], ignore_index=True)

        
        return main_df

    except Exception as e:
        return None
    


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
