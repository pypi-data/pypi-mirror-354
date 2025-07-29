# FluentC LangChain Tool

Official Python plugin for integrating the [FluentC AI Translation API](https://www.fluentc.io) with [LangChain](https://www.langchain.com). This package enables real-time and batch translation, source language detection, and job result polling — all through LangChain-compatible tools.

---

## 🚀 Features

- ✅ Real-Time Translation (`/translate`)
- ⏳ Batch Translation with Auto Polling (`/translate` + `/results`)
- 🌍 Language Detection (`/checklanguage`)
- 📡 Job Result Retrieval (`/results`)
- 🔐 Secure API Key Authentication

---

## 📦 Installation

```bash
pip install fluentc-langchain-tool
```

---

## 🔐 Authentication

You'll need your FluentC API key (provided after signup and subscription):

```python
tool = FluentCTranslationTool(api_key="your-fluentc-api-key")
```

---

## 🧠 Available Tools

| Tool Class | Purpose |
|------------|---------|
| `FluentCTranslationTool` | Real-time or batch translation submit |
| `FluentCLanguageDetectorTool` | Detect source language from input |
| `FluentCTranslationStatusTool` | Check status of batch translation jobs |
| `FluentCResultsTool` | Poll for batch job translation result (legacy) |
| `FluentCBatchTranslationTool` | One-shot batch submit + polling |

---

## 🛠 Real-Time Translation

```python
from fluentc_langchain_tool import FluentCTranslationTool

tool = FluentCTranslationTool(api_key="your-api-key")
response = tool.run({
    "text": "Hello, world!",
    "target_language": "fr",
    "source_language": "en",
    "mode": "realtime"
})
print(response)  # "Bonjour, le monde !"
```

---

## ⏳ Batch Translation (Async with Auto Polling)

```python
from fluentc_langchain_tool import FluentCBatchTranslationTool

tool = FluentCBatchTranslationTool(api_key="your-api-key")

result = tool.run({
    "text": "<html>Hello, batch world!</html>",
    "target_language": "de",
    "source_language": "en"
})

print(result)  # Final translated output after polling
```

✅ Polling automatically respects FluentC's `estimated_wait_seconds` to avoid overloading the API.

---

## 🌍 Language Detection

```python
from fluentc_langchain_tool import FluentCLanguageDetectorTool

tool = FluentCLanguageDetectorTool(api_key="your-api-key")
response = tool.run({
    "text": "Hola, ¿cómo estás?"
})
print(response)  # Detected language: es (confidence: 0.99)
```

---

## 📡 Check Translation Status

```python
from fluentc_langchain_tool import FluentCTranslationStatusTool

tool = FluentCTranslationStatusTool(api_key="your-api-key")
response = tool.run({
    "job_id": "your-job-id"
})
print(response)
```

---

## 🔗 LangChain Agent Integration

```python
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from fluentc_langchain_tool import (
    FluentCTranslationTool,
    FluentCBatchTranslationTool,
    FluentCLanguageDetectorTool,
    FluentCTranslationStatusTool
)

api_key = "your-api-key"

agent = initialize_agent(
    tools=[
        Tool.from_function(FluentCTranslationTool(api_key)),
        Tool.from_function(FluentCBatchTranslationTool(api_key)),
        Tool.from_function(FluentCLanguageDetectorTool(api_key)),
        Tool.from_function(FluentCTranslationStatusTool(api_key))
    ],
    llm=OpenAI(temperature=0),
    agent="zero-shot-react-description"
)

agent.run("Translate 'Hello world' from English to German using FluentC.")
```
