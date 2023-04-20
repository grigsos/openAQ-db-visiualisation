import boto3
import zipfile #to unzip package
import os # to give permissions to engine

from constants import TABLE_NAME, REGION_NAME, DEPLOYMENT_FILE, S3_BUCKET_NAME, LOCAL_FILE, initialize_s3_bucket

dynamodb = boto3.resource('dynamodb', region_name=REGION_NAME) # set up table
table = dynamodb.Table(TABLE_NAME) #get table

def lambda_handler(event, context):
    download_and_setup_zip()
    filter_and_plot()
    cleanup()
    return {
        "statusCode": 200,
        "body": {
            "message": "Data plotted and added successfully"
        }
    }



def download_and_setup_zip():
    bucket = initialize_s3_bucket()
    s3_file = DEPLOYMENT_FILE
    local_file = '/tmp/deployment_package.zip'
    bucket.download_file(s3_file, local_file) #@download deployment file
    with zipfile.ZipFile(local_file, 'r') as zip_ref: #unzip
        zip_ref.extractall('/tmp/deployment_package')  
    os.chmod('/tmp/deployment_package/kaleido/executable/kaleido', 0o755) #give image engine permission
    os.chmod('/tmp/deployment_package/kaleido/executable/bin/kaleido', 0o755) #give image engine permission
    os.sys.path.insert(0, '/tmp/deployment_package') #make it part of runtime environment
    return None
    


def filter_and_plot():
    from visualisation import plot_item #only after downloading of package
    
    filter_params = ['pm1', 'um100', 'pm10', 'pm25', 'um010', 'um025', 'um100']
    
    for param in filter_params:
        items = query_table(param)
        if items:
            plot_item(items, param)



#############Helper function###########
def query_table(param): #query the table
    
    expression = 'parameter_name = :value'
    attribute_values = {':value': param}
    
    response = table.scan(
        FilterExpression=expression,
        ExpressionAttributeValues=attribute_values
    )
    items = response['Items']
    return items
    
def cleanup():
    # Delete the extracted folder and .zip file
    if os.path.exists('/tmp/deployment_package'):
        os.system('rm -rf /tmp/deployment_package')
    if os.path.exists('/tmp/deployment_package.zip'):
        os.remove('/tmp/deployment_package.zip')




