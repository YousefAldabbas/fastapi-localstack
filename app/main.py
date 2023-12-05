from fastapi import FastAPI
import boto3
import localstack_client.session
app = FastAPI()



# localstack_endpoint = "http://127.0.0.1:4566"
# aws_region = "us-east-1"


# sqs = boto3.client("sqs", endpoint_url=localstack_endpoint, region_name=aws_region)
# queue_url = f"http://sqs.eu-central-1.localhost.localstack.cloud:4566/000000000000/localstack-queue"


session = localstack_client.session.Session()
sqs = session.client("sqs")
queue = sqs.create_queue(QueueName="localstack-queue")
queue_url = queue["QueueUrl"]
aws_region = queue_url.split(".")[1]



@app.post("/push_message")
async def push_message(message: str):
    sqs.send_message(QueueUrl=queue_url, MessageBody=message)
    return {"message": "Message pushed to the queue"}


@app.get("/consume_message")
async def consume_message():
    response = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1)
    if "Messages" in response:
        message = response["Messages"][0]
        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message["ReceiptHandle"])
        return {"message": message["Body"]}
    else:
        return {"message": "No messages available"}
