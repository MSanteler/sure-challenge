import boto3

# Initialize a session using Amazon S3
s3 = boto3.client('s3')

def main(dry_run=True, num_prefixes_to_keep=2, bucket_name=''):
    # Get the list of prefixes in the root of the bucket
    response = s3.list_objects_v2(Bucket=bucket_name, Delimiter='/')

    prefixes = []
    if 'CommonPrefixes' in response:
        for prefix in response['CommonPrefixes']:
            prefix_name = prefix['Prefix']
            prefix_response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix_name) # Need an explicit second call for metadata such as last_modified
            last_modified_date = prefix_response['Contents'][0]['LastModified']
            key = prefix_response['Contents'][0]['Key']
            prefixes.append((prefix_name, last_modified_date, key))

    # Sort prefixes by last modified date (newest first)
    prefixes.sort(key=lambda x: x[1], reverse=True)

    # Slice to keep the n most recent prefixes
    prefixes_to_delete = prefixes[num_prefixes_to_keep:]

    # TODO: Additional filtering by date arg

    # Delete the remaining prefixes
    for prefix in prefixes_to_delete:
        if dry_run:
            print(f"DRY RUN: Would delete prefix: {prefix[0]}")
        else:
            print(f"Deleting: {prefix[0]}")
            s3.delete_object(Bucket=bucket_name, Key=prefix[2])

    print('Cleanup complete')

if __name__ == "__main__":
    main(dry_run=True, num_prefixes_to_keep=1, bucket_name='sure-deploys')
