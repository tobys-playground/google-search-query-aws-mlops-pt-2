## BYOC GPT-Neo + AWS MLOps Part 2 (SageMaker + Step Functions + CodePipeline)

## Architecture

![image](https://user-images.githubusercontent.com/81354022/156029599-5d241136-8122-41df-8f1c-ff3e6c27d504.png)

This part of the MLOps (Maturity level 3) workflow focuses on the **second CodePipeline (shaded in orange)** that will create a new custom Training/Inference image when there is a change to the code, and train and deploy a **Bring-Your-Own-Container GPT-Neo model** with this image.

## Steps

1) A commit made to the **GitHub/CodeCommit** repository will trigger the **CodePipeline** and start the **CodeBuild** job
2) **CodeBuild** will create a **new custom Docker Training/Inference image** that will be pushed to **Elastic Container Registry**:

![image](https://user-images.githubusercontent.com/81354022/156136278-7d5e6ac2-1161-464f-81f2-71b71d450d43.png)

3) A **Lambda function** will then **start the Step Functions State Machine** managed by the first CodePipeline (Link to Repo: https://github.com/tobys-playground/google-search-results-aws-mlops-pt-1). Alternatively, a change to the data stored in a **S3 bucket** will also start the State Machine
4) The GPT-Neo model will be trained and deployed as an endpoint in **SageMaker** using our custom image. If this is successful, the State Machine should look as below:

![image](https://user-images.githubusercontent.com/81354022/156136036-c43ad1ec-1276-418f-b069-0128eb308be4.png)

5) CodePipeline will wait for the user's approval before continuing. The user can check to see if the model, endpoint config, and endpoint (Should be **InService**) are in SageMaker:

![image](https://user-images.githubusercontent.com/81354022/156136369-61ab4238-df22-4fe8-abb1-129bfc4d3edb.png)

![image](https://user-images.githubusercontent.com/81354022/156136489-422a834d-9d77-4212-8ea7-2d9417dbb044.png)

![image](https://user-images.githubusercontent.com/81354022/156136580-1e8c145a-49c6-4ed7-8dc5-1fc4d41189ba.png)

6) Once approved, CodePipeline will run a **Lambda function** to store training and artifact details in a simple Model Registry powered by **DynamoDB**:

![image](https://user-images.githubusercontent.com/81354022/156136202-661d8e85-671a-4fa0-8a8b-181dbdb7bcfb.png)

7) Finally, CodePipeline will **run another Lambda function to create/update a Lambda Function and an API Gateway via CloudFormation** so that users can invoke the SageMaker endpoint over the Internet (Note that the API Gateway is not active now):

![image](https://user-images.githubusercontent.com/81354022/156136719-09b83e0c-c6a9-46ba-b755-7fd25a255d58.png)
