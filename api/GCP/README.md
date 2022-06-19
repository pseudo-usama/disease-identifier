# GCP function

## Files
 - [main.py](main.py) contains the code for our GCP cloud function.
 - [requirements.txt](requirements.txt) is used by GCP to install dependencies.


## How to deploy

> gcloud functions deploy predict --runtime python38 --trigger-http --memory MEMORY_IN_BYTES --project YOUR_PROJECT_NAME
