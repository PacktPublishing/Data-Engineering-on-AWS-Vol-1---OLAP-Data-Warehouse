import boto3
import argparse, time

def send_data_to_kinesis(region,stream_arn,file):
    kinesis_producer_client = boto3.client('kinesis',region)
    stream_arn = stream_arn
    input_file = file

    count = 0
    records = list()

    with open(input_file) as file:
        for line in file.readlines():
            order_id = line.split(',')[0]
            data = {
                'Data': line.encode(),
                'PartitionKey': order_id
            }
            records.append(data)
            count = count + 1
            if count == 100:
                kinesis_producer_client.put_records(
                    Records = records,
                    StreamARN = stream_arn
                )
                print('100 records sent to kinesis stream... sleeping for 5 mins')
                time.sleep(300)
                count = 0
                records = []

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-arn",required=True)
    parser.add_argument("-file",required=True)
    parser.add_argument("-region",required=True)

    args = parser.parse_args()
    region=args.region
    stream_arn=args.arn
    file=args.file
    
    send_data_to_kinesis(region,stream_arn,file)
    
