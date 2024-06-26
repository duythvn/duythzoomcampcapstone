# duythzoomcampcapstone
capstone project for Data Engineering zoomcap 


I - Project Name

Data Engineering Pipeline - Custom Support Ticket Report




II - Objective

The objective of this project is to create a data engineering pipeline to ingest customer support tickets of a company and provide detailed analysis through graphs/charts and reports.

From the data, support managers can understand more about how well the support team has been performing. If the company's SLA has been met, and if there are rooms for improvements

The project simulate a data batch processing pipeline and make good uses for MageAI for data ochestration and Looker for dahsboard visulisation




III - dataset and data analysis

#Dataset
customer_support_tickets.csv is provided for demonstrative purposes.


#Data analysis
- Our assumption  is tickets are auto received  & reponded within the first 30 mins and we will use first_response_time as the time when the  tickets are received
- A dashboard has been built to help analyse a few important questions in the Customer Service Department such as
- How many tickets received past few months to understand ticket volume. The info can be used for bechmarking & resource planning purposes
- Customer satisfaction rating from a rank  of  1 to 5: with 5 being the highest rating score
- Time to be resolved and correlation with customer satisfaction rating
(Due to privacy, I have chosen to included a pdf report exported from Google Looker instead)





IV- Tech

The project was built to support both online & local run.

We'll use a combination of Cloud technology, IaC, Data lake, Dat Ochestration, Data warehouse and transformation for demonstrative purposes

In real life scenarios, the full approach will be:

- (OPTIONAL STEP) Monthly Raw data files on S3: will be published by a 3rd party  or another client/user.

We'll make use of AWS serverless (Python Lambda) and Event Bridge to retrieve data from S3 and upload to an SFTP (as per client's requirements, files are kept on SFTP for logging/review purposes)

Although this step is optional, a python file (s3-sftp-lambda.py) and cloudformation yaml  file have been provided to demonstate  how to utilise cloud technology and IaC in this project
please also pip install boto3 and aws_lambda_powertools

- Data is  cleaned uploaded to a Google Cloud Storage Lake
- Data is then transformred and ingested to Big Query
- Final visulisation is presented via Google Looker

![image](https://github.com/duythvn/duythzoomcampcapstone/assets/14797941/f3bf682f-5df6-49bf-937c-061f485c7ffd)


If you want to test this locally, please follow these steps:


##Clone the repository:
git clone https://github.com/duythvn/duythzoomcampcapstone.git

#Install required dependencies:
pip install -r requirements.txt

#MageAI Data ochestration is done using MageAI https://github.com/mage-ai/mage-ai#%EF%B8%8F-quick-start

##You can either install Mage on your local
pip install mage-ai

##Or preferrably,  use docker
docker pull mageai/mageai:latest

#An external dashboard such as Google looker or Power BI is required





V - Set up

#Copy the Mage pipeline and all blocks as per below
Copy Mage "de_zoomcamp_capstone" pipeline to pipelines/de_zoomcamp_capstone in your Mage installation folder

Copy all the other blocks into the respective data_loaders, transformers and data_exporters folder  in your Mage installation

#Update mage  io_config.yaml , create a Mage profile called "dev" and update the below variables. SFTP variables are mostly used to download dataset from source destination

#raw data file: 
Can be found under raw-data folder

dev:
  GOOGLE_SERVICE_ACC_KEY_FILEPATH: "GoogleACCKEY.json"
  
  GOOGLE_LOCATION: US    
  
  SFTP_HOST: testSFTP_HOST
  
  SFTP_PORT: SFTP_PORT
  
  SFTP_USER: SFTP_USER
  
  SFTP_PASSWORD: SFTP_PASSWORD



VI - Findings

![image](https://github.com/duythvn/duythzoomcampcapstone/assets/14797941/212c06ea-d946-4ee0-9de5-34f76ed533e5)




VII - Contributing Guidelines

This repository is for demonstrative purposes only, and contributions are not expected. However, feel free to share any improvements or modifications for learning purposes.



VIII - Known Issues/Limitations/Documentation

Demo data is limited (1 quarter data from a made-up company).

If you encounter any bugs or have feature requests, feel free to share them for learning purposes.

Additional documentation, including API documentation and user guides, is not available for this demo project.





