import boto3
import uuid
import os
import json

step_function = boto3.client('stepfunctions')
code_pipeline = boto3.client('codepipeline')

def lambda_handler(event, context):
    
    job_id = event['CodePipeline.job']['id']
    
    workflow_id = str(uuid.uuid1())

    inputs = {
             'JobName': 'GPTNeo-BYOC-{}'.format(uuid.uuid1().hex), 
             'ModelName': 'GPTNeo-BYOC-{}'.format(uuid.uuid1().hex), 
             'ArtifactLocation': os.environ['ARTIFACT_LOCATION'] + '{}'.format(uuid.uuid1().hex),   
             'EndpointName': 'GPTNeo-BYOC-{}'.format(uuid.uuid1().hex),    
             'DataLocation': os.environ['DATA_LOCATION']
            }
            

    try:
        
        start_workflow = step_function.start_execution(
                                                stateMachineArn = os.environ['STATE_MACHINE_ARN'],
                                                name = workflow_id,
                                                input = json.dumps(inputs)
        )

        code_pipeline.put_job_success_result(jobId = job_id, outputVariables = {'JobName': inputs['JobName'], 
                                                                                'ModelName': inputs['ModelName'],
                                                                                'ArtifactLocation': inputs['ArtifactLocation'],
                                                                                'EndpointName': inputs['EndpointName']})                                      
    except Exception as e:
        print(e)
        print('Function failed due to exception.') 
        code_pipeline.put_job_failure_result(jobId = job_id, failureDetails={'message': 'The Step Function failed to start', 'type': 'JobFailed'})
      
    print('Function complete.')