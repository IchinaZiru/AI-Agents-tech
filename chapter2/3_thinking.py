import boto3
import os
from dotenv import load_dotenv

load_dotenv()

client = boto3.client("bedrock-runtime",region_name="ap-northeast-1")

# Converse APIを実行
response = client.converse(
    modelId="jp.anthropic.claude-sonnet-4-5-20250929-v1:0",
    messages=[{
        "role": "user",
        "content": [{
            "text": "こんにちは"
        }]
    }],
    additionalModelRequestFields={
        "thinking": {
            "type": "enabled",      # 拡張思考をオン
            "budget_tokens": 1024   # 思考トークンの予算
        },
    },
)

# 思考プロセスと最終回答を表示
for content in response["output"]["message"]["content"]:
    if "reasoningContent" in content:
        print("<thinking>")
        print(content["reasoningContent"]["reasoningText"]["text"])
        print("</thinking>")
    elif "text" in content:
        print(content["text"])