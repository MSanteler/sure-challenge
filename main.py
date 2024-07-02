import argparse
import boto3
from botocore.exceptions import ClientError

# Initialize a session using Amazon S3
s3 = boto3.client('s3')

def get_prefix_metadata(bucket_name, prefix_name):
    try:
        prefix_response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix_name)
        if 'Contents' in prefix_response:
            return (prefix_name, prefix_response['Contents'][0]['LastModified'], prefix_response['Contents'][0]['Key'])
        print(f"Error missing metadata {prefix_name}: {e}")
        exit(1)
    except ClientError as e:
        print(f"Error fetching s3 metadata for {prefix_name}: {e}")
        exit(1)

def positive_nonzero_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError(f"{value} is invalid. Must be a positive non-zero integer value")
    return ivalue

def main(dry_run=True, num_prefixes_to_keep=2, bucket_name=''):
    num_prefixes_to_keep = positive_nonzero_int(num_prefixes_to_keep) # Redundant validation in case main is somehow invoked outside of the cli
    # Get the list of prefixes in the root of the bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')
    except ClientError as e:
        print(f"Error fetching s3 data for {bucket_name}: {e}")
        exit(1)

    prefixes = []
    if 'CommonPrefixes' in response:
        for prefix in response['CommonPrefixes']:
            prefix_name = prefix['Prefix']
            prefix_metadata = get_prefix_metadata(bucket_name, prefix_name)
            if prefix_metadata:
                prefixes.append(prefix_metadata)

    # Sort prefixes by last modified date (newest first)
    prefixes.sort(key=lambda x: x[1], reverse=True)

    # Slice to keep the n most recent prefixes
    prefixes_to_delete = prefixes[num_prefixes_to_keep:]

    # TODO: Additional filtering by date arg e.g.
    # filter_date = datetime(2024, 6, 30)
    # prefixes_to_delete = [prefix for prefix in prefixes_to_delete if prefix[1] < filter_date]

    # Delete the remaining prefixes by key
    for prefix in prefixes_to_delete:
        if dry_run:
            print(f"DRY RUN: Would delete prefix: {prefix[0]}")
        else:
            print(f"Deleting: {prefix[0]}")
            try:
                s3.delete_object(Bucket=bucket_name, Key=prefix[2])
            except ClientError as e:
                print(f"Error deleting from key: {prefix[2]} from {bucket_name}: {e}")

    print('Cleanup complete')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean up old S3 prefixes (deploys).')
    parser.add_argument('-n', '--num-prefixes-to-keep', type=positive_nonzero_int, default=3, help='Number of recent prefixes to keep (must be a positive non-zero integer)')
    parser.add_argument('-d', '--dry-run', action='store_true', help='Perform a dry run without deleting anything')
    parser.add_argument('-b', '--bucket-name', type=str, required=True, help='The name of the S3 bucket')

    args = parser.parse_args()
    main(args.dry_run, args.num_prefixes_to_keep, args.bucket_name)