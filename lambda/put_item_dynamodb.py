import boto3

code_pipeline = boto3.client('codepipeline')
dynamodb = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    job_id = event['CodePipeline.job']['id']
    
    field_list = event["CodePipeline.job"]['data']['actionConfiguration']['configuration']['UserParameters'].split(', ')
    
    try:
        dynamodb.put_item(
            TableName='ModelRegistry', 
            Item={
                'JobName':{
                    'S': field_list[0]
                },
                'ModelName':{
                    'S': field_list[1]
                },
                'ArtifactLocation':{
                    'S': field_list[2]
                },
                'EndpointName':{
                    'S': field_list[3]
                },
                'Status':{
                    'S': 'Deployed'
                }
            }
        )
        code_pipeline.put_job_success_result(jobId = job_id)
        
    except Exception as e:
        print(e)
        print('Function failed due to exception.') 
        code_pipeline.put_job_failure_result(jobId = job_id, failureDetails={'message': 'Insertion into Model Registry failed', 'type': 'JobFailed'})