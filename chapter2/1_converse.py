# 必要なライブラリをインポート
import boto3
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Bedrock呼び出し用のAPIクライアントを作成
client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))

# Converse APIを実行
response = client.converse(
    modelId="anthropic.claude-3-5-sonnet-20240620-v1:0", # モデルID
    messages=[{
        "role": "user",
        "content": [{
            "text": "こんにちは" # 入力メッセージ
        }]
    }]
)

# 実行結果のテキストだけを画面に表示
print(response["output"]["message"]["content"][0]["text"])