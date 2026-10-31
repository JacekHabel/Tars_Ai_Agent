# TARS - Local AI Agent with Tool Calling and Voice Control

TARS is a local AI agent in Python that uses an LLM (Qwen3 8B via Ollama) to interpret commands and call tools: Google Calendar, an ESP32-C3 + BME280 sensor, and later voice input (Whisper).

Final project for a Python programming laboratory course. **Work in progress.**

## Goal

Build a system that actually performs actions, not just a chatbot. Responsibilities are separated:

- **LLM**: interprets the user's intent and proposes a tool call.
- **Python application**: validates the request, controls execution, manages the workflow.
- **Tools**: communicate with external APIs and hardware.

The model has no direct access to the operating system. Every action goes through a tool registry that validates arguments against a JSON Schema.

## Planned pipeline

```
Speech -> Whisper -> text -> Qwen3 8B -> tool selection -> validation -> Python tool -> response
```

## Status

| Stage | Description | Status |
|-------|-------------|--------|
| 1 | Basic agent: tool registry, validation, text commands | In progress  |
| 2 | Google Calendar integration | Planned |
| 3 | ESP32-C3 + BME280 sensor | Planned |
| 4 | Qwen3 8B via Ollama | Planned |
| 5 | Voice input (Whisper) | Planned |
| 6 | Tests, error handling, documentation | Planned |

## Notes

- Hardware: GMKtec NucBox K8 Plus (Ryzen 7 8845HS, 32 GB RAM), Ubuntu Server, Docker.
- Credentials and tokens are never committed (`.env`, `credentials.json`, `token.json` are in `.gitignore`).
