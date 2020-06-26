import sys

# import boto3
import subprocess


def gen_filename(account_name: str) -> str:
    return "twitter-@" + account_name + "-filtered.txt"


accounts = []
if __name__ == "__main__":
    for count, line in enumerate(sys.stdin):
        if count == 0:
            account_name = line.split("twitter.com/")[1].split("/")[0]
            current_account = account_name
            f = open("jobs/" + gen_filename(account_name), "w")
            f.write(line)

            accounts.append(account_name)

        elif line.split("twitter.com/")[1].split("/")[0] == current_account:
            f.write(line + "\n")

        else:
            f.close()
            account_name = line.split("twitter.com/")[1].split("/")[0]
            current_account = account_name
            f = open("jobs/" + gen_filename(account_name), "w")
            f.write(line)

            if account_name not in accounts:
                accounts.append(account_name)

    f.close()

    # sqs = boto3.client("sqs")
    # queue_uri = sqs.get_queue_url(QueueName="queuebot.fifo").get('QueueUrl')
    with open("jobs/jobs.txt", "w") as f:
        for each_account in accounts:
            uri = str(
                subprocess.run(
                    "curl --upload-file jobs/{filename} https://transfer.notkiska.pw/{filename}".format(
                        filename=gen_filename(each_account)
                    ),
                    shell=True,
                    capture_output=True,
                ).stdout.decode()
            )
            # print("Added", uri, each_account, "to queue", queue_uri)
            f.write(uri + "\n")
            print("Added", uri)

            # response = sqs.send_message(
            # QueueUrl=queue_uri,
            # MessageAttributes={
            # "Twitter-Account": {"DataType": "String", "StringValue": str(each_account)},
            # },
            # MessageBody=str(uri),
            # MessageGroupId='queuebot',
            # MessageDeduplicationId=str(each_account)
            # )
    print(
        "Jobs list",
        subprocess.run(
            "curl --upload-file jobs/{filename} https://transfer.notkiska.pw/{filename}".format(
                filename="jobs.txt"
            ),
            shell=True,
            capture_output=True,
        ).stdout.decode()
    )
