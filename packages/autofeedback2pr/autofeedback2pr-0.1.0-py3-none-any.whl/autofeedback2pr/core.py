import os
import requests
import json

PROMPT_TEMPLATE = {
    'en': '''\
You are an AI assistant. A user has submitted the following feedback:
"""{feedback}"""

Classify the feedback into one of the following types: [Feature, Bug, UX].
Then, rate the difficulty of fixing this (1-10).
Explain briefly, and provide a confidence score (0-100).
Respond in JSON format like:
{{
  "type": "Bug",
  "difficulty": 6,
  "confidence": 85,
  "explanation": "Likely a missing event handler."
}}
''',
    'zh': '''\
你是一个AI助手。用户提交了以下反馈：
"""{feedback}"""

请将其分类为以下三类之一：[功能, Bug, 体验]。
然后评估修复难度（1-10），并简单解释原因。
请提供一个信心值（0-100）。
请使用如下 JSON 格式回复：
{{
  "type": "Bug",
  "difficulty": 6,
  "confidence": 85,
  "explanation": "可能是事件处理器未绑定。"
}}
'''
}

API_URL = "https://api.anthropic.com/v1/messages"
API_KEY = None

SUPPORTED_LANGUAGES = ['en', 'zh']

def config(api_key: str):
    """配置 Claude API Key。"""
    global API_KEY
    API_KEY = api_key

def build_prompt(feedback, lang):
    return PROMPT_TEMPLATE.get(lang, PROMPT_TEMPLATE['en']).format(feedback=feedback)

def grade_feedback(feedback, lang="en"):
    key = API_KEY or os.getenv("CLAUDE_API_KEY")
    if not key:
        raise ValueError("Claude API key not set. Use autofeedback2pr.config(api_key=...) or set CLAUDE_API_KEY env var.")
    if lang not in SUPPORTED_LANGUAGES:
        lang = 'en'
    prompt = build_prompt(feedback, lang)
    headers = {
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    body = {
        "model": "claude-3-7-sonnet-latest",
        "max_tokens": 500,
        "temperature": 0.5,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, headers=headers, json=body)
    response.raise_for_status()
    content = response.json()['content'][0]['text']
    # 去除 markdown 代码块包裹
    if content.startswith("```json"):
        content = content[7:]
    if content.endswith("```"):
        content = content[:-3]
    return json.loads(content.strip()) 