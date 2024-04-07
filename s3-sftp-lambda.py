
import json
import boto3

import s3fs
from datetime import datetime   
from pathlib import Path
from paramiko.client import SSHClient
from paramiko import AutoAddPolicy
from aws_lambda_powertools import Logger, Metrics, Tracer
base_path = Path(__file__).parent

file_path = (base_path / "./config.json").resolve()

#please replace with the proper s3 and sftp path
SOURCE_PATH="S3 SOURCE PATH"
DESTINATION_PATH=""+"/RAW/"

s3 = s3fs.S3FileSystem(anon=False)

tracer = Tracer(service='APP')
logger = Logger(service='APP')
     

def sftp_send(event, context):
    try:
    
       
        if event :
         
            file_names=download_s3_file(SOURCE_PATH)
            if file_names == None:
                return
            sftp_client = SSHClient()
            sftp_client.set_missing_host_key_policy(AutoAddPolicy())
            
            #please replace with proper SFTP details
            sftp_client.connect(hostname="FTP_HOST",
            port="FTP_PORT",
            username="FTP_USERNAME",
            password="FTP_PASSWORD")
            sftp_handle = sftp_client.open_sftp()
            for file_name in file_names:
           
          
                destination="/"+ DESTINATION_PATH +file_name
            
            
                try:
                    sftp_handle.put(file_name,destination)
                 
                except Exception as e:
                    logger.exception('SFTPHelper - transfer_file - ' + str(e))
                    raise
        else:
            logger.info("'SFTP - sftp_send - no event found so function was not triggered")
        return {
            "statusCode": 200,
            "body": "maropostsftp - usftp_send - completed"
        }
    except Exception as e:
        logger.exception('maropostsftp - sftp_send - ' + str(e))
        return {"statusCode": 400, "body": json.dumps({"message": str(e)})}
        





def download_s3_file():
    try:
     
        s3_file = s3fs.S3FileSystem(anon=False)
        if SOURCE_PATH == None:
            return None            
        else:
         
            files = s3.ls(SOURCE_PATH)

        file_names=[]
        for file in files:
            if '.csv' in file or '.json' in file:
                file_name=file.rsplit('/', 1)[-1]
                destination_file='/tmp/'+file_name
            
                s3.download(file,destination_file)
                file_names.append(destination_file)
       
    except Exception as e:
   
        raise
    