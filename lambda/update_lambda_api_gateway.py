import boto3
import os

code_pipeline = boto3.client('codepipeline')
cloudformation_update = boto3.client('cloudformation')

def lambda_handler(event, context):
    
    job_id = event['CodePipeline.job']['id']
    
    field_list = event["CodePipeline.job"]['data']['actionConfiguration']['configuration']['UserParameters'].split(', ')
    
    parameter_value = field_list[3]
    
    try:
        response = cloudformation_update.update_stack(StackName=os.environ['STACK_NAME'], 
                                                UsePreviousTemplate = True,
                                                Parameters =[
                                                                {
                                                                    'ParameterKey': 'EndPointName',
                                                                    'ParameterValue': parameter_value
                                                                },
                                                                {
                                                                    'ParameterKey': 'ApiGatewayStageName',
                                                                    'UsePreviousValue' : True
                                                                }
                                                            ],
                                                Capabilities = ['CAPABILITY_NAMED_IAM', 'CAPABILITY_NAMED_IAM'],
                                                RoleARN = os.environ['ROLE_ARN'])
                                                
        code_pipeline.put_job_success_result(jobId = job_id)                                                  
        
        print('Stack update succeeded!')                    
    except Exception as e:
        print(e)
        print('Function failed due to exception.') 
        code_pipeline.put_job_failure_result(jobId = job_id, failureDetails={'message': 'Cloudformation stack update failed', 'type': 'JobFailed'})
