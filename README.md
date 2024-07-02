# Sure Infrastructure Scripting Challenge

* This script uses boto3 and assumes that the host has set AWS credentials via env vars
* Create a test bucket and populate with local sample-data
  ```
  aws s3api create-bucket --bucket sure-deploys --region us-east-1
  ```
  ```
  aws s3 sync sample-data s3://sure-deploys --delete
  ```
* Run the script
  ```
  python ./main.py
  ```

# Original Prompt:
# Infrastructure Scripting Challenge

As a member of the Infrastructure team, I want to cleanup old deployment folders in s3 to help manage AWS costs.

Write a script to remove all but the most recent X deployments. The script should take in X as a parameter.

If a deployment is older than X deployments, we will delete the entire folder.

S3 folder bucket assets will look similar to below. 

```json
s3-bucket-name
	deployhash112/index.html
				 /css/font.css
				 /images/hey.png 
	dsfsfsl9074/root.html
				 /styles/font.css
				 /img/hey.png 
  delkjlkploy3/base.html
				 /fonts/font.css
				 /png/hey.png 
  dsfff1234321/...
  klljkjkl123/...
```

## Questions

1. Where should we run this script? 
2. How should we test the script before running it production?
3. If we want to add an additional requirement of deleting deploys older than X days but we must maintain at least Y number of deploys. What additional changes would you need to make in the script?

## Notes

Write the script in a high-level programming language such as python/nodejs (we prefer python).

Consider using localstack to mimic s3.

List any assumptions made in a README.md.

Please provide the github repo of the scripting project.