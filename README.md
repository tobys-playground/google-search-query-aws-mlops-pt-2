## BYOC GPT-Neo + AWS MLOps Part 2 (SageMaker + Step Functions + CodePipeline)

## Architecture

![image](https://user-images.githubusercontent.com/81354022/156029599-5d241136-8122-41df-8f1c-ff3e6c27d504.png)

This part of the MLOps workflow focuses on the **second CodePipeline (shaded in orange)** that will create a new custom Training/Inference image when there is a change to the code, and train and deploy a **Bring-Your-Own-Container GPT-Neo model** with this image.

## Steps

1) A commit made to the **GitHub/CodeCommit** repository will trigger the **CodePipeline** and start the **CodeBuild** job
2) **CodeBuild** will create a **new custom Docker Training/Inference image** that will be pushed to **Elastic Container Registry**:

![image](https://user-images.githubusercontent.com/81354022/156123733-5a580bed-c608-4aa8-8bba-079148980ba0.png)

3) A **Lambda function** will then **start the Step Functions State Machine** managed by the first CodePipeline (Link to Repo: https://github.com/tobys-playground/google-search-results-aws-mlops-pt-1). Alternatively, a change to the data stored in a **S3 bucket** will also start the State Machine
4) The GPT-Neo model will be trained and deployed as an endpoint in **SageMaker** using our custom image. If this is successful, the State Machine should look as below:

![image](https://user-images.githubusercontent.com/81354022/156123180-45aa4bc0-d79d-45b7-b202-30c8711550b6.png)

5) CodePipeline will wait for the user's approval before continuing. The user can check to see if the model, endpoint config, and endpoint (Should be **InService**) are in SageMaker:

![image](https://user-images.githubusercontent.com/81354022/156123835-a03f30ec-8c6e-4148-9af1-257e63900f2b.png)

![image](https://user-images.githubusercontent.com/81354022/156124020-b58824eb-7876-4d65-a58f-5a1d1d1fc382.png)

![image](https://user-images.githubusercontent.com/81354022/156124166-ff6de5c0-d0b6-4a1d-998e-708da733a8a6.png)

6) Once approved, CodePipeline will run a **Lambda function** to store training and artifact details in a simple Model Registry powered by **DynamoDB**:

![image](https://user-images.githubusercontent.com/81354022/156123366-373389c6-ea72-4c09-998c-74cb14c65b14.png)

7) Finally, CodePipeline will **run another Lambda function to create/update a Lambda Function and an API Gateway via CloudFormation** so that users can invoke the SageMaker endpoint over the Internet (Note that the API Gateway is not active now):

![image](https://user-images.githubusercontent.com/81354022/156123512-9a826d47-cdcf-48ea-bc55-ce382b37b119.png)
