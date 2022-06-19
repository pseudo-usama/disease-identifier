We've developed an webapp from where anyone can use our model. But the ML model is not build and shipped to the webapp. So thats why we need to develop an API that enables webapp to make predictions.

There're two implementations of this api:
 - [FastAPI](FastAPI/): Implementation of api using FastAPI. 
 - [GCP](GCP/): Implementation of api for GCP.

The reason of two different implementation is that 2nd one can only be used by GCP cannot run localy. But 1st implementation is using FastAPI which can be run localy and also on other hosting services.
