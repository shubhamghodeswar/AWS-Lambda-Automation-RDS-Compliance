import json
import boto3
import botocore.exceptions

def lambda_handler(event, context):
    instanceList = []
    tagKey = ''
    tagValue = ''
    client = boto3.client('rds')
    response = client.describe_db_instances()['DBInstances']
    for instance in response:
        try:
            if(instance['TagList'] == []):
                # do nothing
            else:
                for i in instance['TagList']:
                    if(i['Key'] == 'approved_by' and i['Value'] == 'wba-cso'):
                        tagKey = i['Key']
                        tagValue = i['Value']
            
            if(tagKey == 'approved_by' and tagValue = 'wba-cso'):
                # DO NOTHING
            else:
                if(str(instance['StorageEncrypted']) == 'False'):
                    instanceList.append(instance['DBInstanceIdentifier'])
            
                if(str(instance['PubliclyAccessible']) == 'True'):      # Blocking public access if found publicly accesible
                    responsepub = client.modify_db_instance(
                        PubliclyAccessible = False    
                    )    
                
            
            
        except client.exceptions.ClientError as e:
            print("Error occured")
            
    send_rds_mail(instanceList)
    


def send_rds_mail(instances):
    if(instances == []):
        rdsStr = 'All instances are encrypted'
    else:
        rdsStr = '\n'.join(map(str, instances))
        rdsStr = '\n' + rdsStr + ' \n \nThe above instances do not have encryption enabled'
    ses_client = boto3.client('ses')
    ses_client.send_email(
        Source = 'enter source email ID',
        Destination = {
            'ToAddresses': ['enter list of recipient email IDs']
        },
        Message = {
            'Subject': {
                'Data': 'RDS Encryption Notification',
                'Charset': 'utf-8'
            },
            'Body': {
                'Text': {
                    'Data': rdsStr
                }
            }
        }
    )
    
