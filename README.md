## BYOC GPT-Neo + AWS MLOps Part 2 (SageMaker + Step Functions + CodePipeline)

## Architecture

![image](https://user-images.githubusercontent.com/81354022/156029599-5d241136-8122-41df-8f1c-ff3e6c27d504.png)

This part of the MLOps workflow focuses on the second CodePipeline (shaded in orange) that will create a new custom Training/Inference image when there is a change to the code, and train and deploy a Bring-Your-Own-Container GPT-Neo model with this image.

## Steps

1) A commit made to the **GitHub/CodeCommit** repository will trigger the CodePipeline and start the CodeBuild job
2) **CodeBuild** will create a **new custom Docker Training/Inference image** that will be pushed to **Elastic Container Registry**
3) A **Lambda function** will then **start the Step Functions State Machine** managed by the first CodePipeline (Link to Repo: ). Alternatively, a change to the data stored in an **S3 bucket** will also start the State Machine. 
4) The GPT-Neo model will be trained and deployed as an endpoint in **SageMaker** using our custom image. If this is successful, the State Machine should look as below:


5) CodePipeline will wait for the user's approval before continuing. The user can check to see if the model and endpoint are in SageMaker

6) Once approved, CodePipeline will run a **Lambda function** to store training and artifact details in a simple Model Registry powered by **DynamoDB** 
7) Finally, CodePipeline will **run another Lambda function to create a Lambda Function and an API Gateway via CloudFormation** so that users can invoke the SageMaker endpoint over the Internet.
