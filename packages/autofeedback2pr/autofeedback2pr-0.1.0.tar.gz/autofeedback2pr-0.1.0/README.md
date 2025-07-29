# autofeedback2pr

自动化分析用户反馈并生成结构化 JSON，适合集成到开发者工作流。

## 安装

```bash
pip install .
```

## 使用方法

```python
import autofeedback2pr

autofeedback2pr.config(api_key="YOUR_CLAUDE_KEY")
result = autofeedback2pr.grade_feedback("The button does not work on mobile.", lang="en")
print(result)
```

- Claude API Key 可通过 `autofeedback2pr.config(api_key=...)` 或设置环境变量 `CLAUDE_API_KEY`。 