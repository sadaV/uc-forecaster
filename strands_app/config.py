import os
USE_BEDROCK = os.getenv("USE_BEDROCK", "false").lower() == "true"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BEDROCK_MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
DATA_DIR = "data"
OUT_DIR = "outputs"
