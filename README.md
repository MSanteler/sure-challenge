# Sure Infrastructure Scripting Challenge

## Running the script
* This script uses boto3 and assumes that the host has set AWS credentials via a [supported configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/configuration.html)
* End to end test easily with the following commands
  * Verify python is installed
    ```
    ❯ python -V
    Python 3.12.4
    ```
  * Create a test bucket and populate with local sample-data
    ```
    aws s3api create-bucket --bucket sure-deploys --region us-east-1
    ```
    ```
    aws s3 sync sample-data s3://sure-deploys --delete
    ```
  * Run the script
    ```
    python ./main.py --bucket-name sure-deploys -n 2 --dry-run
    ```
  * Use the `--help` flag to learn more about the expected args
    ```
    python ./main.py --help
    ```

## Questions
1. Where should we run this script? 
    - This would be a good candidate for running in a lambda, which can be easily triggered each time a new deploy a new artifact is pushed to the bucket, but could be run wherever an organization prefers to run their containerized jobs such as in kubernetes as a cron, or an argo workflow, or as part of a deployment pipeline.
2. How should we test the script before running it production?
    - The `--dry-run` option is included to facilitate testing. It could be deployed to production with `--dry-run` enabled for a few cycles, and the logs reviewed before fully deploying. A few unit tests could also be written to verify the scripted behavior by stubbing out the boto3 calls, perhaps using [moto](https://docs.getmoto.org/en/latest/docs/getting_started.html), or localstack as mentioned.
3. If we want to add an additional requirement of deleting deploys older than X days but we must maintain at least Y number of deploys. What additional changes would you need to make in the script?
    - I included a [TODO](https://github.com/MSanteler/sure-challenge/commit/3bef1b816f0344d1e724e2c9507d399efbc3c456#diff-b10564ab7d2c520cdd0243874879fb0a782862c3c902ab535faabe57d5a505e1R25-R27), as well as a quick example of how to achieve this in the code. It would be a simple enough change – since the first thing we do after sorting by last_modified is slice out the required number of prefixes, we can safely utilize the additional filtering without worrying about deleting too many entries.
    - In addition to the two lines shown, we would of course need to add the datetime library, as well as a new argument to pass through the script
    - We may want to consider the edge cases more closely with the additional argument, and add more validation

<br>
<br>

---
# Original Prompt:
---

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