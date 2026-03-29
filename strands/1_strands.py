from strands import Agent
from dotenv import load_dotenv

#env読み込み
load_dotenv()

#エージェントを作成、起動
agent = Agent("us.anthropic.claude-sonnet-4-20250514-v1:0")
agent("Strandsってどういう意味？")