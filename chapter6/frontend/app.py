import os, asyncio, boto3
import streamlit as st
from dotenv import load_dotenv
from agent_executor import invoke

# 明示的に .env ファイルを指定して読み込み
load_dotenv('.env', override=True)

# デバッグ: 環境変数が正しく読み込まれているか確認
if not os.getenv('AWS_REGION'):
    st.error("❌ エラー: AWS_REGION 環境変数が設定されていません")
    st.stop()

# タイトル表示
st.title("AWS開発お助けエージェント")
st.write("AWSドキュメントや、あなたのアカウントの調査をお手伝いします!")

# セッションを初期化
if 'messages' not in st.session_state:
    st.session_state.messages = []
    
# メッセージ履歴を表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# AgentCore APIクライアントを初期化
# AWS マネージドランタイムを使用（CodeBuild でデプロイ済み）
agent_core = boto3.client(
    'bedrock-agentcore',
    region_name=os.getenv('AWS_REGION')
)

# ユーザー入力を表示
if prompt := st.chat_input("メッセージを入力してください"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    # エージェントの応答を表示
    with st.chat_message("assitant"):
        container = st.container()
        try:
            response = asyncio.run(
                invoke(prompt, container, agent_core)
            )
            if response:
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
