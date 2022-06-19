# FastAPI Server

Contains the implementation of api using FastAPI.

## How to run
Just run [main.py](main.py) as normal python file. It will host an server on port `8080`.
> http://localhost:8080





docker run -t --rm -p 8501:8501 -v "D:\Project\potato-disease\models:/models" tensorflow/serving --rest_api_port=8501 --model_config_file="/models/models.config"